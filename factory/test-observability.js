#!/usr/bin/env node

/**
 * Test script for Software Factory Observability
 * Run this to verify the observability system is working
 */

const { trackAIAnalysis, trackAIError, trackTestRun, trackGenericEvent } = require('./observability');

async function testObservability() {
  console.log('🧪 Testing Software Factory Observability...\n');

  try {
    // Test AI analysis tracking
    console.log('📊 Testing AI analysis tracking...');
    await trackAIAnalysis({
      app: 'test-app',
      service: 'openai',
      status: 'success',
      fallbackUsed: false,
      processingTimeMs: 1250,
      metadata: {
        model: 'gpt-4',
        tokens: 1500,
        test: true
      }
    });
    console.log('✅ AI analysis event tracked');

    // Test AI error tracking
    console.log('❌ Testing AI error tracking...');
    await trackAIError({
      app: 'test-app',
      service: 'openai',
      status: 'failure',
      fallbackUsed: true,
      processingTimeMs: 5000,
      error: 'Rate limit exceeded',
      metadata: {
        model: 'gpt-4',
        retryCount: 3,
        test: true
      }
    });
    console.log('✅ AI error event tracked');

    // Test test run tracking
    console.log('🧪 Testing test run tracking...');
    await trackTestRun({
      app: 'test-app',
      pipeline: 'e2e-tests',
      status: 'pass',
      details: 'All 15 tests passed successfully'
    });
    console.log('✅ Test run event tracked');

    // Test generic event tracking
    console.log('📝 Testing generic event tracking...');
    await trackGenericEvent({
      app: 'test-app',
      name: 'test_event',
      payload: {
        userId: 'test-user-123',
        action: 'test_action',
        timestamp: new Date().toISOString(),
        test: true
      }
    });
    console.log('✅ Generic event tracked');

    console.log('\n🎉 All observability tests completed successfully!');
    console.log('Check your Supabase dashboard to see the tracked events.');

  } catch (error) {
    console.error('❌ Observability test failed:', error.message);
    
    if (error.message.includes('Supabase credentials missing')) {
      console.log('\n💡 To fix this:');
      console.log('1. Run: source scripts/load-factory-env.sh');
      console.log('2. Or set environment variables manually:');
      console.log('   export FACTORY_SUPABASE_URL=https://your-project.supabase.co');
      console.log('   export FACTORY_SUPABASE_SERVICE_KEY=your-service-key');
    }
    
    process.exit(1);
  }
}

// Run the test
testObservability();
