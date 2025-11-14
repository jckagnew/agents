/**
 * Retry Utilities
 * Provides retry logic with exponential backoff for external API calls
 */

export interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableErrors?: string[];
}

export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  initialDelayMs: 1000,
  maxDelayMs: 10000,
  backoffMultiplier: 2,
  retryableErrors: [
    'ECONNRESET',
    'ETIMEDOUT',
    'ENOTFOUND',
    'ECONNREFUSED',
    '429', // Rate limit
    '500', // Internal server error
    '502', // Bad gateway
    '503', // Service unavailable
    '504', // Gateway timeout
  ],
};

/**
 * Retry a function with exponential backoff
 * Useful for handling transient failures in external API calls
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY_CONFIG
): Promise<T> {
  let lastError: Error;
  let delayMs = config.initialDelayMs;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Check if error is retryable
      const errorString = lastError.message.toLowerCase();
      const errorCode = (lastError as any).code;

      const isRetryable = config.retryableErrors?.some(
        (retryableError) =>
          errorString.includes(retryableError.toLowerCase()) ||
          errorCode === retryableError
      );

      // Don't retry on last attempt or if error is not retryable
      if (!isRetryable || attempt === config.maxRetries) {
        throw lastError;
      }

      console.warn(
        `Attempt ${attempt + 1}/${config.maxRetries} failed: ${lastError.message}. Retrying in ${delayMs}ms...`
      );

      // Wait before retry
      await new Promise((resolve) => setTimeout(resolve, delayMs));

      // Exponential backoff
      delayMs = Math.min(
        delayMs * config.backoffMultiplier,
        config.maxDelayMs
      );
    }
  }

  throw lastError!;
}

/**
 * Safely parse JSON from a Response object
 * Handles parsing errors gracefully with detailed error messages
 */
export async function safeJSONParse<T = any>(response: Response): Promise<T> {
  try {
    const text = await response.text();

    if (!text || text.trim().length === 0) {
      throw new Error('Empty response body');
    }

    try {
      return JSON.parse(text) as T;
    } catch (parseError) {
      const errorMessage =
        parseError instanceof Error ? parseError.message : String(parseError);
      throw new Error(
        `JSON parse error: ${errorMessage}. Response preview: ${text.substring(0, 200)}`
      );
    }
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to parse JSON response: ${errorMessage}`);
  }
}

/**
 * Setup global error handlers for unhandled promise rejections
 * Call this once in your application entry point
 */
export function setupGlobalErrorHandlers(): void {
  // Handle unhandled promise rejections
  process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Promise Rejection:');
    console.error('  Promise:', promise);
    console.error('  Reason:', reason);

    // Log stack trace if available
    if (reason instanceof Error && reason.stack) {
      console.error('  Stack:', reason.stack);
    }

    // In production, you might want to:
    // 1. Send to error tracking service (Sentry, DataDog, etc.)
    // 2. Exit process and let PM2/Kubernetes restart
    // process.exit(1);
  });

  // Handle uncaught exceptions
  process.on('uncaughtException', (error) => {
    console.error('❌ Uncaught Exception:');
    console.error('  Error:', error.message);
    console.error('  Stack:', error.stack);

    // In production, exit and restart
    // process.exit(1);
  });

  console.log('✅ Global error handlers initialized');
}
