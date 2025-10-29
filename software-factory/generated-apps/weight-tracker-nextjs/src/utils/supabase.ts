/**
 * Supabase utility for hostname-based database configuration
 * Maps different DBA domains to their respective Supabase projects
 */

import { createClient } from '@supabase/supabase-js';

// Hostname to Supabase configuration mapping
// NOTE: Hostnames use neutral placeholders (consumer/bespoke/enterprise).
// Swap in real DBA domains if each joint venture needs a distinct identifier.
const HOSTNAME_TO_SUPABASE_CONFIG: Record<string, { url: string; anonKey: string }> = {
  'consumer.clevelsalesguy.com': {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  },
  'bespoke.clevelsalesguy.com': {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  },
  'enterprise.clevelsalesguy.com': {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  },
  'localhost': {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  },
};

/**
 * Get the appropriate Supabase client based on current hostname
 */
export function getSupabaseClient() {
  if (typeof window === 'undefined') {
    // Server-side: use default config
    const config = HOSTNAME_TO_SUPABASE_CONFIG['localhost'];
    return createClient(config.url, config.anonKey);
  }

  const hostname = window.location.hostname;
  const config = HOSTNAME_TO_SUPABASE_CONFIG[hostname] || HOSTNAME_TO_SUPABASE_CONFIG['localhost'];
  
  return createClient(config.url, config.anonKey);
}

/**
 * Get the brand context for database operations
 */
export function getBrandContext() {
  if (typeof window === 'undefined') {
    return 'consumer';
  }

  const hostname = window.location.hostname;
  const brandMap: Record<string, string> = {
    'consumer.clevelsalesguy.com': 'consumer',
    'bespoke.clevelsalesguy.com': 'bespoke',
    'enterprise.clevelsalesguy.com': 'enterprise',
    'localhost': 'consumer',
  };

  return brandMap[hostname] || brandMap['localhost'];
}

/**
 * Create a brand-aware database query
 */
export function createBrandQuery(table: string, brand?: string) {
  const client = getSupabaseClient();
  const brandContext = brand || getBrandContext();
  
  return client
    .from(table)
    .select('*')
    .eq('brand', brandContext);
}

/**
 * Insert data with brand context
 */
export async function insertWithBrand(table: string, data: Record<string, any>) {
  const client = getSupabaseClient();
  const brandContext = getBrandContext();
  
  return client
    .from(table)
    .insert({
      ...data,
      brand: brandContext,
      created_at: new Date().toISOString(),
    });
}

/**
 * Update data with brand context
 */
export async function updateWithBrand(table: string, id: string, data: Record<string, any>) {
  const client = getSupabaseClient();
  const brandContext = getBrandContext();
  
  return client
    .from(table)
    .update({
      ...data,
      brand: brandContext,
      updated_at: new Date().toISOString(),
    })
    .eq('id', id)
    .eq('brand', brandContext);
}

/**
 * Delete data with brand context
 */
export async function deleteWithBrand(table: string, id: string) {
  const client = getSupabaseClient();
  const brandContext = getBrandContext();
  
  return client
    .from(table)
    .delete()
    .eq('id', id)
    .eq('brand', brandContext);
}
