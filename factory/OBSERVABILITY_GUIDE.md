# Software Factory Observability System

This guide explains how to use the Software Factory's observability system to track AI events, test runs, and generic events across all projects created by the factory.

## Quick Start

### 1. Load Environment Variables

In any project's terminal, run:

```bash
source scripts/load-factory-env.sh
```

This script will:
- Read factory-related Supabase values from `.env`
- Prompt for any missing keys
- Export them (including Expo mirrors) into your shell
- Make observability helpers work immediately

### 2. Set Up Your .env File

Create a `.env` file in your project root with the following variables:

```bash
# Factory Observability (Required)
FACTORY_SUPABASE_URL=https://your-project.supabase.co
FACTORY_SUPABASE_SERVICE_KEY=your-service-role-key
# OR use anon key for client-side apps
FACTORY_SUPABASE_ANON_KEY=your-anon-key

# Expo/React Native mirrors (auto-created by script)
EXPO_PUBLIC_FACTORY_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_FACTORY_SUPABASE_SERVICE_KEY=your-service-role-key
EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY=your-anon-key
```

## Database Schema

The observability system uses the following Supabase tables:

### factory_apps
- `id` (uuid): Primary key
- `slug` (text): Unique app identifier
- `name` (text): Human-readable app name
- `repo` (text): Repository URL (optional)
- `created_at` (timestamptz): Creation timestamp

### factory_ai_events
- `id` (uuid): Primary key
- `app` (text): App identifier
- `service` (text): AI service name
- `status` (text): 'success' or 'failure'
- `fallback_used` (boolean): Whether fallback was used
- `processing_time_ms` (integer): Processing time in milliseconds
- `metadata` (jsonb): Additional event data
- `created_at` (timestamptz): Event timestamp

### factory_ai_errors
- Same as `factory_ai_events` plus:
- `error` (text): Error message

### factory_test_runs
- `id` (uuid): Primary key
- `app` (text): App identifier
- `pipeline` (text): Test pipeline name
- `status` (text): 'pass' or 'fail'
- `details` (text): Additional details
- `created_at` (timestamptz): Test run timestamp

### factory_generic_events
- `id` (uuid): Primary key
- `app` (text): App identifier
- `name` (text): Event name
- `payload` (jsonb): Event data
- `created_at` (timestamptz): Event timestamp

## Usage Examples

### TypeScript/JavaScript Projects

```typescript
import { trackAIAnalysis, trackAIError, trackTestRun, trackGenericEvent } from '../factory/observability';

// Track AI analysis success
await trackAIAnalysis({
  app: 'weight-tracker',
  service: 'openai',
  status: 'success',
  fallbackUsed: false,
  processingTimeMs: 1250,
  metadata: {
    model: 'gpt-4',
    tokens: 1500,
    confidence: 0.95
  }
});

// Track AI analysis failure
await trackAIError({
  app: 'weight-tracker',
  service: 'openai',
  status: 'failure',
  fallbackUsed: true,
  processingTimeMs: 5000,
  error: 'Rate limit exceeded',
  metadata: {
    model: 'gpt-4',
    retryCount: 3
  }
});

// Track test run
await trackTestRun({
  app: 'weight-tracker',
  pipeline: 'e2e-tests',
  status: 'pass',
  details: 'All 15 tests passed successfully'
});

// Track generic event
await trackGenericEvent({
  app: 'weight-tracker',
  name: 'user_registration',
  payload: {
    userId: 'user_123',
    plan: 'pro',
    source: 'mobile_app'
  }
});
```

### React Native/Expo Projects

```javascript
// In your React Native app
import { trackAIAnalysis, trackGenericEvent } from '../lib/observability';

// Track AI events in your components
const handleAIAnalysis = async () => {
  const startTime = Date.now();
  
  try {
    const result = await analyzeWithAI(data);
    
    await trackAIAnalysis({
      app: 'weight-tracker-mobile',
      service: 'openai',
      status: 'success',
      fallbackUsed: false,
      processingTimeMs: Date.now() - startTime,
      metadata: {
        model: 'gpt-4',
        inputLength: data.length
      }
    });
    
    return result;
  } catch (error) {
    await trackAIError({
      app: 'weight-tracker-mobile',
      service: 'openai',
      status: 'failure',
      fallbackUsed: true,
      processingTimeMs: Date.now() - startTime,
      error: error.message,
      metadata: {
        model: 'gpt-4',
        retryCount: 0
      }
    });
    
    throw error;
  }
};
```

### Python Projects

```python
import os
import requests
import json
from datetime import datetime

def track_ai_analysis(app, service, status, fallback_used, processing_time_ms, metadata=None):
    """Track AI analysis event"""
    url = os.getenv('FACTORY_SUPABASE_URL')
    key = os.getenv('FACTORY_SUPABASE_SERVICE_KEY')
    
    if not url or not key:
        print(f"[factory] {app} - {service} - {status}")
        return
    
    endpoint = f"{url}/rest/v1/factory_ai_events"
    headers = {
        'Content-Type': 'application/json',
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Prefer': 'return=minimal'
    }
    
    payload = {
        'app': app,
        'service': service,
        'status': status,
        'fallback_used': fallback_used,
        'processing_time_ms': processing_time_ms,
        'metadata': metadata or {}
    }
    
    try:
        requests.post(endpoint, headers=headers, json=payload)
    except Exception as e:
        print(f"[factory] Failed to track event: {e}")

# Usage
track_ai_analysis(
    app='weight-tracker',
    service='openai',
    status='success',
    fallback_used=False,
    processing_time_ms=1250,
    metadata={'model': 'gpt-4', 'tokens': 1500}
)
```

## Integration Patterns

### 1. AI Service Wrapper

```typescript
class AIService {
  constructor(private appName: string) {}
  
  async analyze(data: any, options: any = {}) {
    const startTime = Date.now();
    
    try {
      const result = await this.callAI(data, options);
      
      await trackAIAnalysis({
        app: this.appName,
        service: 'openai',
        status: 'success',
        fallbackUsed: false,
        processingTimeMs: Date.now() - startTime,
        metadata: {
          model: options.model || 'gpt-4',
          inputLength: JSON.stringify(data).length
        }
      });
      
      return result;
    } catch (error) {
      await trackAIError({
        app: this.appName,
        service: 'openai',
        status: 'failure',
        fallbackUsed: true,
        processingTimeMs: Date.now() - startTime,
        error: error.message,
        metadata: {
          model: options.model || 'gpt-4',
          retryCount: options.retryCount || 0
        }
      });
      
      throw error;
    }
  }
}
```

### 2. Test Runner Integration

```typescript
async function runTests(appName: string, testSuite: string) {
  const startTime = Date.now();
  
  try {
    const results = await executeTests(testSuite);
    
    await trackTestRun({
      app: appName,
      pipeline: testSuite,
      status: results.passed ? 'pass' : 'fail',
      details: `Tests: ${results.passed}/${results.total} passed`
    });
    
    return results;
  } catch (error) {
    await trackTestRun({
      app: appName,
      pipeline: testSuite,
      status: 'fail',
      details: `Test execution failed: ${error.message}`
    });
    
    throw error;
  }
}
```

### 3. User Event Tracking

```typescript
// Track user interactions
const trackUserAction = async (action: string, data: any) => {
  await trackGenericEvent({
    app: 'weight-tracker',
    name: `user_${action}`,
    payload: {
      userId: getCurrentUserId(),
      timestamp: new Date().toISOString(),
      ...data
    }
  });
};

// Usage in components
const handleButtonClick = () => {
  trackUserAction('button_click', {
    buttonId: 'analyze-weight',
    screen: 'dashboard'
  });
};
```

## Monitoring and Analytics

### Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to Table Editor
3. View the observability tables:
   - `factory_ai_events` - AI service performance
   - `factory_ai_errors` - AI service failures
   - `factory_test_runs` - Test execution results
   - `factory_generic_events` - Custom events

### Common Queries

```sql
-- AI service performance by app
SELECT 
  app,
  service,
  COUNT(*) as total_requests,
  AVG(processing_time_ms) as avg_processing_time,
  SUM(CASE WHEN fallback_used THEN 1 ELSE 0 END) as fallback_count
FROM factory_ai_events 
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY app, service
ORDER BY total_requests DESC;

-- Test run success rate
SELECT 
  app,
  pipeline,
  COUNT(*) as total_runs,
  SUM(CASE WHEN status = 'pass' THEN 1 ELSE 0 END) as passed_runs,
  ROUND(
    SUM(CASE WHEN status = 'pass' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
    2
  ) as success_rate
FROM factory_test_runs 
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY app, pipeline
ORDER BY success_rate DESC;

-- Error trends
SELECT 
  app,
  service,
  error,
  COUNT(*) as error_count,
  MAX(created_at) as last_occurrence
FROM factory_ai_errors 
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY app, service, error
ORDER BY error_count DESC;
```

## Best Practices

1. **Consistent App Naming**: Use consistent app identifiers across all events
2. **Meaningful Metadata**: Include relevant context in metadata fields
3. **Error Context**: Always include error messages and retry counts
4. **Performance Tracking**: Track processing times for optimization
5. **Fallback Detection**: Mark when fallback mechanisms are used
6. **Privacy**: Don't log sensitive user data in payloads

## Troubleshooting

### Environment Variables Not Loading

```bash
# Check if variables are loaded
echo $FACTORY_SUPABASE_URL

# Reload the script
source scripts/load-factory-env.sh

# Check .env file exists and has correct format
cat .env | grep FACTORY_
```

### Events Not Appearing in Database

1. Check Supabase credentials are correct
2. Verify RLS policies allow inserts
3. Check network connectivity
4. Look for error messages in console logs

### Development vs Production

- In development: Events are logged to console if Supabase is unavailable
- In production: Events are sent to Supabase database
- Use `NODE_ENV=production` to enable production mode
