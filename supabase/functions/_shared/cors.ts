/**
 * CORS configuration for Edge Functions
 * SECURITY: Restrict origins in production to your actual domains
 */

// Allowed origins - configure these for your production environment
const ALLOWED_ORIGINS = [
  // Mobile development
  'http://localhost:8081', // Expo dev server
  'exp://localhost:8081', // Expo development

  // Web development
  'http://localhost:19006', // Expo web default port
  'http://localhost:3000', // Alternative local port
  'http://127.0.0.1:19006',
  'http://127.0.0.1:3000',

  // Production domains (uncomment and configure for your deployment)
  // 'https://yourdomain.com',
  // 'https://admin.yourdomain.com',
  // 'https://admin-console.vercel.app', // Vercel
  // 'https://your-site.netlify.app', // Netlify
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
