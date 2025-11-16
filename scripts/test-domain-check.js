#!/usr/bin/env node

/**
 * Test script for domain availability checking
 *
 * This script tests the domain availability implementation without requiring API keys.
 * It will show the graceful fallback behavior when API keys are not configured.
 */

// Import the name vetting module
const { checkDomainAvailability, vetBusinessName } = require('./name-vetting.js');

async function testDomainCheck() {
  console.log('\n🧪 Testing Domain Availability Check\n');
  console.log('=' .repeat(60));

  const testNames = [
    'Acme Corp',
    'Widget Labs',
    'Fathomly',
    'Tech Solutions',
  ];

  for (const name of testNames) {
    console.log(`\nTesting: "${name}"`);
    console.log('-'.repeat(60));

    try {
      // This will test the domain check directly
      // Without API keys, it should gracefully return 'unknown' status
      const result = await vetBusinessName(name);

      console.log('\n📊 Results:');
      console.log(`Score: ${result.score.totalScore}/100 (${result.score.assessment})`);
      console.log(`\nDomain Check:`);
      console.log(`  Available domains: ${result.details.domain.available.length}`);
      console.log(`  Best domain: ${result.details.domain.bestDomain || 'None found'}`);
      console.log(`  Score: ${result.details.domain.score}/40`);
      console.log(`  Notes: ${result.details.domain.notes}`);

      if (result.details.domain.details && result.details.domain.details.length > 0) {
        console.log(`\n  Domain Details:`);
        result.details.domain.details.forEach(d => {
          console.log(`    ${d.domain}: ${d.availability}${d.priceHint ? ` (${d.priceHint})` : ''}`);
        });
      }

    } catch (error) {
      console.error(`❌ Error testing "${name}":`, error.message);
    }

    console.log('\n' + '='.repeat(60));
  }

  console.log('\n✅ Domain availability check test complete!\n');
  console.log('📝 Notes:');
  console.log('  - Without API keys, domains will show "unknown" status');
  console.log('  - To test with real data, set environment variables:');
  console.log('    export DOMAINR_API_KEY="your_key"');
  console.log('    export GODADDY_API_KEY="your_key"');
  console.log('    export GODADDY_API_SECRET="your_secret"');
  console.log('');
}

// Run the test
testDomainCheck().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
