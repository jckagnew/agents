/**
 * Supabase Edge Function: Capture Website Screenshot
 *
 * Captures a screenshot of a website for design analysis
 * Uses Puppeteer or a screenshot API service
 *
 * Deploy with: supabase functions deploy capture-screenshot
 */

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

interface ScreenshotRequest {
  url: string;
  width?: number;
  height?: number;
  fullPage?: boolean;
}

interface ScreenshotResponse {
  screenshot: string; // Base64 encoded PNG
  url: string;
  timestamp: string;
}

/**
 * Main handler
 */
serve(async (req) => {
  try {
    // CORS headers
    if (req.method === 'OPTIONS') {
      return new Response('ok', {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
        },
      });
    }

    // Parse request
    const {
      url,
      width = 1280,
      height = 720,
      fullPage = false,
    }: ScreenshotRequest = await req.json();

    if (!url) {
      return new Response(
        JSON.stringify({ error: 'url is required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Validate URL
    try {
      new URL(url);
    } catch {
      return new Response(
        JSON.stringify({ error: 'Invalid URL provided' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Capture screenshot using a screenshot API service
    // Option 1: Use a service like ScreenshotAPI.net, ApiFlash, etc.
    // Option 2: Use Puppeteer in Deno (requires custom layer)
    //
    // For production, we recommend using a dedicated screenshot service
    // Here's an example using ScreenshotAPI.net:

    const screenshotApiKey = Deno.env.get('SCREENSHOT_API_KEY');

    if (!screenshotApiKey) {
      // Fallback: Return a placeholder for development
      console.warn('SCREENSHOT_API_KEY not configured, returning placeholder');
      return new Response(
        JSON.stringify({
          screenshot: createPlaceholderImage(width, height),
          url,
          timestamp: new Date().toISOString(),
        }),
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    }

    // Use ScreenshotAPI.net or similar service
    const screenshotUrl = new URL('https://shot.screenshotapi.net/screenshot');
    screenshotUrl.searchParams.set('token', screenshotApiKey);
    screenshotUrl.searchParams.set('url', url);
    screenshotUrl.searchParams.set('width', width.toString());
    screenshotUrl.searchParams.set('height', height.toString());
    screenshotUrl.searchParams.set('output', 'image');
    screenshotUrl.searchParams.set('file_type', 'png');
    screenshotUrl.searchParams.set('wait_for_event', 'load');

    if (fullPage) {
      screenshotUrl.searchParams.set('full_page', 'true');
    }

    const response = await fetch(screenshotUrl.toString());

    if (!response.ok) {
      throw new Error(`Screenshot API error: ${response.status}`);
    }

    // Convert to base64
    const arrayBuffer = await response.arrayBuffer();
    const base64 = btoa(
      new Uint8Array(arrayBuffer).reduce(
        (data, byte) => data + String.fromCharCode(byte),
        ''
      )
    );

    const result: ScreenshotResponse = {
      screenshot: base64,
      url,
      timestamp: new Date().toISOString(),
    };

    return new Response(JSON.stringify(result), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    console.error('Screenshot capture error:', error);
    return new Response(
      JSON.stringify({
        error: error.message || 'Failed to capture screenshot',
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  }
});

/**
 * Create a placeholder image for development
 * Returns a simple base64-encoded PNG
 */
function createPlaceholderImage(width: number, height: number): string {
  // This is a minimal 1x1 transparent PNG
  // In production, you would use a proper screenshot service
  const placeholderPNG =
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';

  console.log(`Creating placeholder image (${width}x${height})`);
  return placeholderPNG;
}
