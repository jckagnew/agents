# Software Factory Observability System

This directory contains the observability system for the Software Factory and all projects created by it.

## Quick Start

### 1. Set up observability for a new project

```bash
# Run the setup script
./factory/setup-observability.sh

# Load environment variables
source scripts/load-factory-env.sh
```

### 2. Set up your Supabase database

Run the SQL schema in your Supabase project:

```sql
-- Copy and paste the contents of supabase-observability.sql
-- into your Supabase SQL editor
```

### 3. Start tracking events

```typescript
import { trackAIAnalysis, trackGenericEvent } from './src/lib/observability';

// Track user events
await trackGenericEvent({
  name: 'button_click',
  payload: {
    buttonId: 'analyze',
    screen: 'dashboard'
  }
});

// Track AI analysis
await trackAIAnalysis({
  service: 'openai',
  status: 'success',
  fallbackUsed: false,
  processingTimeMs: 1250,
  metadata: { model: 'gpt-4', tokens: 1500 }
});
```

## Files

- `observability.ts` - TypeScript observability client
- `observability.js` - JavaScript observability client  
- `supabase-observability.sql` - Database schema
- `setup-observability.sh` - Setup script for new projects
- `OBSERVABILITY_GUIDE.md` - Detailed usage guide

## Environment Variables

Add these to your `.env` file:

```bash
FACTORY_SUPABASE_URL=https://your-project.supabase.co
FACTORY_SUPABASE_SERVICE_KEY=your-service-role-key
# OR
FACTORY_SUPABASE_ANON_KEY=your-anon-key
```

## Database Tables

- `factory_apps` - Registered applications
- `factory_ai_events` - AI service events
- `factory_ai_errors` - AI service errors
- `factory_test_runs` - Test execution results
- `factory_generic_events` - Custom events

## Usage Examples

See `OBSERVABILITY_GUIDE.md` for comprehensive examples and integration patterns.

## Monitoring

View your observability data in the Supabase dashboard or run custom queries:

```sql
-- AI service performance
SELECT app, service, AVG(processing_time_ms) as avg_time
FROM factory_ai_events 
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY app, service;
```
