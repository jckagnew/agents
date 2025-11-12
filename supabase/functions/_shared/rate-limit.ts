/**
 * Simple in-memory rate limiter for Edge Functions
 * Prevents brute force and DoS attacks
 *
 * NOTE: This is per-instance. For multi-instance deployments,
 * consider using Upstash Redis or similar distributed solution.
 */

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

const rateLimitMap = new Map<string, RateLimitEntry>();

// Cleanup old entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of rateLimitMap.entries()) {
    if (entry.resetAt < now) {
      rateLimitMap.delete(key);
    }
  }
}, 5 * 60 * 1000);

export interface RateLimitConfig {
  windowMs: number; // Time window in milliseconds
  maxRequests: number; // Max requests per window
}

export const RATE_LIMITS = {
  // Conservative limits for Edge Functions
  strict: { windowMs: 60 * 1000, maxRequests: 10 }, // 10 req/min
  moderate: { windowMs: 60 * 1000, maxRequests: 60 }, // 60 req/min
  relaxed: { windowMs: 60 * 1000, maxRequests: 100 }, // 100 req/min
};

/**
 * Check if request exceeds rate limit
 * @param identifier Unique identifier (user ID, IP, etc.)
 * @param config Rate limit configuration
 * @returns { allowed: boolean, remaining: number, resetAt: number }
 */
export function checkRateLimit(
  identifier: string,
  config: RateLimitConfig = RATE_LIMITS.moderate
): {
  allowed: boolean;
  remaining: number;
  resetAt: number;
  retryAfter?: number;
} {
  const now = Date.now();
  const key = `${identifier}:${Math.floor(now / config.windowMs)}`;

  let entry = rateLimitMap.get(key);

  if (!entry) {
    entry = {
      count: 0,
      resetAt: now + config.windowMs,
    };
    rateLimitMap.set(key, entry);
  }

  entry.count++;

  const allowed = entry.count <= config.maxRequests;
  const remaining = Math.max(0, config.maxRequests - entry.count);
  const retryAfter = allowed ? undefined : Math.ceil((entry.resetAt - now) / 1000);

  return {
    allowed,
    remaining,
    resetAt: entry.resetAt,
    retryAfter,
  };
}

/**
 * Create rate limit response headers
 */
export function getRateLimitHeaders(
  rateLimitInfo: ReturnType<typeof checkRateLimit>,
  config: RateLimitConfig
) {
  return {
    'X-RateLimit-Limit': config.maxRequests.toString(),
    'X-RateLimit-Remaining': rateLimitInfo.remaining.toString(),
    'X-RateLimit-Reset': new Date(rateLimitInfo.resetAt).toISOString(),
    ...(rateLimitInfo.retryAfter
      ? { 'Retry-After': rateLimitInfo.retryAfter.toString() }
      : {}),
  };
}

/**
 * Create rate limit exceeded response
 */
export function rateLimitExceededResponse(
  rateLimitInfo: ReturnType<typeof checkRateLimit>,
  config: RateLimitConfig,
  corsHeaders: Record<string, string>
): Response {
  return new Response(
    JSON.stringify({
      error: 'Too many requests',
      message: `Rate limit exceeded. Try again in ${rateLimitInfo.retryAfter} seconds.`,
      retryAfter: rateLimitInfo.retryAfter,
    }),
    {
      status: 429,
      headers: {
        ...corsHeaders,
        ...getRateLimitHeaders(rateLimitInfo, config),
        'Content-Type': 'application/json',
      },
    }
  );
}
