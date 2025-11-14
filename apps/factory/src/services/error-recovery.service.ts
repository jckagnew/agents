/**
 * Error Recovery Service
 * Provides retry logic and error handling strategies
 *
 * Features:
 * - Exponential backoff retry
 * - Circuit breaker pattern
 * - Fallback strategies
 * - Error classification
 */

export interface RetryOptions {
  maxAttempts?: number;
  initialDelay?: number;
  maxDelay?: number;
  backoffMultiplier?: number;
  retryableErrors?: string[];
}

export interface RecoveryAction {
  action: 'retry' | 'fallback' | 'fail' | 'skip';
  reason: string;
  fallbackValue?: any;
}

export interface CircuitBreakerConfig {
  failureThreshold: number;
  resetTimeout: number;
}

export enum CircuitState {
  CLOSED = 'CLOSED', // Normal operation
  OPEN = 'OPEN', // Failing, reject immediately
  HALF_OPEN = 'HALF_OPEN', // Testing if recovered
}

/**
 * Error Recovery Service
 */
export class ErrorRecoveryService {
  private static instance: ErrorRecoveryService;
  private circuitBreakers: Map<string, {
    state: CircuitState;
    failures: number;
    lastFailure: number;
    config: CircuitBreakerConfig;
  }> = new Map();

  /**
   * Get singleton instance
   */
  static getInstance(): ErrorRecoveryService {
    if (!ErrorRecoveryService.instance) {
      ErrorRecoveryService.instance = new ErrorRecoveryService();
    }
    return ErrorRecoveryService.instance;
  }

  /**
   * Retry a function with exponential backoff
   */
  async retryWithBackoff<T>(
    fn: () => Promise<T>,
    options: RetryOptions = {}
  ): Promise<T> {
    const {
      maxAttempts = 3,
      initialDelay = 1000,
      maxDelay = 30000,
      backoffMultiplier = 2,
      retryableErrors = [],
    } = options;

    let lastError: Error | null = null;
    let delay = initialDelay;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error: any) {
        lastError = error;

        // Check if error is retryable
        if (retryableErrors.length > 0) {
          const isRetryable = retryableErrors.some((errMsg) =>
            error.message.includes(errMsg)
          );
          if (!isRetryable) {
            throw error; // Not retryable, fail immediately
          }
        }

        // Last attempt, throw error
        if (attempt === maxAttempts) {
          throw error;
        }

        // Wait before next attempt
        console.log(
          `Attempt ${attempt}/${maxAttempts} failed: ${error.message}. Retrying in ${delay}ms...`
        );
        await this.sleep(delay);

        // Exponential backoff
        delay = Math.min(delay * backoffMultiplier, maxDelay);
      }
    }

    throw lastError || new Error('Retry failed');
  }

  /**
   * Handle code generation failure
   */
  async handleCodeGenerationFailure(
    jobId: string,
    error: Error
  ): Promise<RecoveryAction> {
    const errorMessage = error.message.toLowerCase();

    // Classify error
    if (this.isTransientError(error)) {
      return {
        action: 'retry',
        reason: 'transient_error',
      };
    }

    if (this.isRateLimitError(error)) {
      return {
        action: 'retry',
        reason: 'rate_limit',
      };
    }

    if (this.isInvalidInputError(error)) {
      return {
        action: 'fail',
        reason: 'invalid_input',
      };
    }

    if (this.isOutOfQuotaError(error)) {
      return {
        action: 'fail',
        reason: 'quota_exceeded',
      };
    }

    // Default: retry once
    return {
      action: 'retry',
      reason: 'unknown_error',
    };
  }

  /**
   * Execute with circuit breaker
   */
  async executeWithCircuitBreaker<T>(
    key: string,
    fn: () => Promise<T>,
    config: CircuitBreakerConfig = {
      failureThreshold: 5,
      resetTimeout: 60000, // 1 minute
    }
  ): Promise<T> {
    // Initialize circuit breaker if not exists
    if (!this.circuitBreakers.has(key)) {
      this.circuitBreakers.set(key, {
        state: CircuitState.CLOSED,
        failures: 0,
        lastFailure: 0,
        config,
      });
    }

    const breaker = this.circuitBreakers.get(key)!;

    // Check circuit state
    if (breaker.state === CircuitState.OPEN) {
      // Check if reset timeout has passed
      const now = Date.now();
      if (now - breaker.lastFailure > breaker.config.resetTimeout) {
        // Move to half-open state
        breaker.state = CircuitState.HALF_OPEN;
        breaker.failures = 0;
      } else {
        throw new Error(`Circuit breaker OPEN for ${key}`);
      }
    }

    try {
      // Execute function
      const result = await fn();

      // Success - reset circuit
      if (breaker.state === CircuitState.HALF_OPEN) {
        breaker.state = CircuitState.CLOSED;
      }
      breaker.failures = 0;

      return result;
    } catch (error) {
      // Failure - increment counter
      breaker.failures++;
      breaker.lastFailure = Date.now();

      // Check if threshold exceeded
      if (breaker.failures >= breaker.config.failureThreshold) {
        breaker.state = CircuitState.OPEN;
      }

      throw error;
    }
  }

  /**
   * Execute with fallback
   */
  async executeWithFallback<T>(
    primary: () => Promise<T>,
    fallback: () => Promise<T> | T
  ): Promise<T> {
    try {
      return await primary();
    } catch (error) {
      console.warn('Primary execution failed, using fallback:', error);
      return typeof fallback === 'function' ? await fallback() : fallback;
    }
  }

  /**
   * Classify errors
   */
  private isTransientError(error: Error): boolean {
    const transientPatterns = [
      'network',
      'timeout',
      'econnrefused',
      'econnreset',
      'etimedout',
      'temporarily unavailable',
    ];

    return transientPatterns.some((pattern) =>
      error.message.toLowerCase().includes(pattern)
    );
  }

  private isRateLimitError(error: Error): boolean {
    const rateLimitPatterns = ['rate limit', 'too many requests', '429'];

    return rateLimitPatterns.some((pattern) =>
      error.message.toLowerCase().includes(pattern)
    );
  }

  private isInvalidInputError(error: Error): boolean {
    const invalidInputPatterns = [
      'invalid input',
      'validation failed',
      'bad request',
      '400',
    ];

    return invalidInputPatterns.some((pattern) =>
      error.message.toLowerCase().includes(pattern)
    );
  }

  private isOutOfQuotaError(error: Error): boolean {
    const quotaPatterns = ['quota exceeded', 'limit exceeded', '403'];

    return quotaPatterns.some((pattern) =>
      error.message.toLowerCase().includes(pattern)
    );
  }

  /**
   * Helper: Sleep utility
   */
  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Get circuit breaker status
   */
  getCircuitBreakerStatus(key: string): {
    state: CircuitState;
    failures: number;
  } | null {
    const breaker = this.circuitBreakers.get(key);
    if (!breaker) return null;

    return {
      state: breaker.state,
      failures: breaker.failures,
    };
  }

  /**
   * Reset circuit breaker manually
   */
  resetCircuitBreaker(key: string): void {
    const breaker = this.circuitBreakers.get(key);
    if (breaker) {
      breaker.state = CircuitState.CLOSED;
      breaker.failures = 0;
      breaker.lastFailure = 0;
    }
  }
}

/**
 * Singleton instance
 */
let errorRecoveryServiceInstance: ErrorRecoveryService | null = null;

export function getErrorRecoveryService(): ErrorRecoveryService {
  if (!errorRecoveryServiceInstance) {
    errorRecoveryServiceInstance = new ErrorRecoveryService();
  }

  return errorRecoveryServiceInstance;
}
