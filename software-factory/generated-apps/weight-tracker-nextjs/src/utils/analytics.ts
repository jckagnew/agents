/**
 * Analytics utility for hostname-based GA4 tracking
 * Maps different DBA domains to their respective GA4 measurement IDs
 */

// Hostname to GA4 ID mapping
// NOTE: Hostnames use neutral placeholders (consumer/bespoke/enterprise).
// Replace with actual DBA domains when naming is finalized or per joint venture.
const HOSTNAME_TO_GA4_ID: Record<string, string> = {
  'consumer.clevelsalesguy.com': process.env.NEXT_PUBLIC_GA4_CONSUMER_ID || '',
  'bespoke.clevelsalesguy.com': process.env.NEXT_PUBLIC_GA4_BESPOKE_ID || '',
  'enterprise.clevelsalesguy.com': process.env.NEXT_PUBLIC_GA4_ENTERPRISE_ID || '',
  'localhost': process.env.NEXT_PUBLIC_GA4_CONSUMER_ID || '', // Default to consumer for local dev
};

// Brand mapping for analytics events
const HOSTNAME_TO_BRAND: Record<string, string> = {
  'consumer.clevelsalesguy.com': 'consumer',
  'bespoke.clevelsalesguy.com': 'bespoke',
  'enterprise.clevelsalesguy.com': 'enterprise',
  'localhost': 'consumer', // Default to consumer for local dev
};

/**
 * Get the appropriate GA4 measurement ID based on current hostname
 */
export function getGA4Id(): string {
  if (typeof window === 'undefined') {
    return process.env.NEXT_PUBLIC_GA4_CONSUMER_ID || '';
  }

  const hostname = window.location.hostname;
  return HOSTNAME_TO_GA4_ID[hostname] || HOSTNAME_TO_GA4_ID['localhost'];
}

/**
 * Get the brand name for analytics events
 */
export function getBrandName(): string {
  if (typeof window === 'undefined') {
    return 'consumer';
  }

  const hostname = window.location.hostname;
  return HOSTNAME_TO_BRAND[hostname] || HOSTNAME_TO_BRAND['localhost'];
}

/**
 * Track a custom event with brand context
 */
export function trackEvent(eventName: string, parameters?: Record<string, any>) {
  if (typeof window === 'undefined') return;

  const brand = getBrandName();
  const eventData = {
    event: eventName,
    brand,
    timestamp: new Date().toISOString(),
    ...parameters,
  };

  // Send to GA4 if available
  if (typeof window.gtag !== 'undefined') {
    window.gtag('event', eventName, {
      custom_parameter_brand: brand,
      ...parameters,
    });
  }

  // Also log for debugging
  console.log('Analytics Event:', eventData);
}

/**
 * Track page views with brand context
 */
export function trackPageView(pagePath: string) {
  if (typeof window === 'undefined') return;

  const brand = getBrandName();
  
  if (typeof window.gtag !== 'undefined') {
    window.gtag('config', getGA4Id(), {
      page_path: pagePath,
      custom_map: {
        brand: brand,
      },
    });
  }

  console.log('Page View:', { brand, path: pagePath });
}

// Extend Window interface for gtag
declare global {
  interface Window {
    gtag: (...args: any[]) => void;
  }
}
