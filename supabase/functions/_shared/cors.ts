/**
 * CORS configuration for Edge Functions
 * SECURITY: Restrict origins in production to your actual domains
 */

// Allowed origins - configure these for your production environment
const ALLOWED_ORIGINS = [
  'http://localhost:8081', // Expo dev server
  'exp://localhost:8081', // Expo development
  // Add your production domains here:
  // 'https://yourdomain.com',
  // 'https://admin.yourdomain.com',
];

/**
 * Get CORS headers with origin validation
 */
export function getCorsHeaders(req: Request) {
  const origin = req.headers.get('origin') || '';

  // Check if origin is allowed
  const isAllowed = ALLOWED_ORIGINS.some(allowed =>
    origin === allowed || origin.startsWith(allowed)
  );

  return {
    'Access-Control-Allow-Origin': isAllowed ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    'Access-Control-Max-Age': '86400', // 24 hours
  };
}

// Backward compatibility - use first allowed origin as default
export const corsHeaders = {
  'Access-Control-Allow-Origin': ALLOWED_ORIGINS[0],
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

/**
 * Handle CORS preflight requests with proper origin validation
 */
export function handleCors(req: Request): Response | null {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: getCorsHeaders(req) });
  }
  return null;
}
