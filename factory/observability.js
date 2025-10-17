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

function buildRestUrl(table) {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    if (!IS_PROD) {
      console.info('[factory] Supabase credentials missing; logging locally only.');
    }
    return null;
  }
  const base = SUPABASE_URL.endsWith('/') ? SUPABASE_URL.slice(0, -1) : SUPABASE_URL;
  return `${base}/rest/v1/${table}`;
}

async function post(table, payload) {
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

function trackAIAnalysis(event) {
  return post('factory_ai_events', event);
}

function trackAIError(event) {
  return post('factory_ai_errors', event);
}

function trackTestRun(event) {
  return post('factory_test_runs', event);
}

function trackGenericEvent(event) {
  return post('factory_generic_events', event);
}

module.exports = {
  trackAIAnalysis,
  trackAIError,
  trackTestRun,
  trackGenericEvent,
};
