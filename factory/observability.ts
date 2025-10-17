export type AIEventStatus = 'success' | 'failure';

export interface FactoryAIEvent {
  app: string;
  service: string;
  status: AIEventStatus;
  fallbackUsed: boolean;
  processingTimeMs: number;
  metadata?: Record<string, unknown>;
}

export interface FactoryAIError extends FactoryAIEvent {
  error?: string;
}

export interface FactoryTestRun {
  app: string;
  pipeline: string;
  status: 'pass' | 'fail';
  details?: string;
}

export interface FactoryGenericEvent {
  app: string;
  name: string;
  payload?: Record<string, unknown>;
}

const SUPABASE_URL =
  process.env.FACTORY_SUPABASE_URL ||
  process.env.NEXT_PUBLIC_SUPABASE_URL ||
  process.env.SUPABASE_URL ||
  '';

const SUPABASE_KEY =
  process.env.FACTORY_SUPABASE_SERVICE_KEY ||
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  process.env.FACTORY_SUPABASE_ANON_KEY ||
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
  '';

const IS_PROD = process.env.NODE_ENV === 'production';

function buildRestUrl(table: string): string | null {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    if (!IS_PROD) {
      console.info('[factory] Supabase credentials missing; logging locally only.');
    }
    return null;
  }
  const base = SUPABASE_URL.endsWith('/') ? SUPABASE_URL.slice(0, -1) : SUPABASE_URL;
  return `${base}/rest/v1/${table}`;
}

async function post(table: string, payload: unknown): Promise<void> {
  const endpoint = buildRestUrl(table);
  if (!endpoint) {
    if (!IS_PROD) {
      console.debug('[factory]', table, payload);
    }
    return;
  }

  try {
    await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
        Prefer: 'return=minimal',
      },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    if (!IS_PROD) {
      console.warn('[factory] failed to write event', table, error);
    }
  }
}

export function trackAIAnalysis(event: FactoryAIEvent): Promise<void> {
  return post('factory_ai_events', event);
}

export function trackAIError(event: FactoryAIError): Promise<void> {
  return post('factory_ai_errors', event);
}

export function trackTestRun(event: FactoryTestRun): Promise<void> {
  return post('factory_test_runs', event);
}

export function trackGenericEvent(event: FactoryGenericEvent): Promise<void> {
  return post('factory_generic_events', event);
}
