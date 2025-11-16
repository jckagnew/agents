#!/usr/bin/env node

/**
 * Test script for the Social Handle Availability functionality
 * Tests the new social media platform checks
 */

// Load environment variables
require('dotenv').config();

// Import the checkSocialHandles function
const { checkSocialHandles } = require('./name-vetting.js');

async function testSocialHandles() {
  console.log('🧪 Testing Social Handle Availability Implementation\n');

  // Test cases
  const testNames = [
    'Fathomly',           // Should be available on most platforms
    'Quillan',            // Should be available on most platforms
    'Apple',              // Should be taken on all platforms
    'Microsoft',          // Should be taken on all platforms
    'TestCompany12345',   // Should be available (random)
    'Google'              // Should be taken on all platforms
  ];

  for (const name of testNames) {
    console.log(`\n📱 Testing: "${name}"`);
    console.log('─'.repeat(50));
    
    try {
      const result = await checkSocialHandles(name);
      
      console.log(`🔗 Primary Handle: ${result.handle}`);
      console.log(`📊 Available Count: ${result.availableCount}/3`);
      console.log(`⭐ Score: ${result.score}/20`);
      console.log(`📝 Notes: ${result.notes}`);
      
      console.log('\n📱 Platform Status:');
      Object.entries(result.platformAvailability).forEach(([platform, status]) => {
        const emoji = status === 'available' ? '✅' : status === 'taken' ? '❌' : '⚠️';
        console.log(`   ${emoji} ${platform}: ${status}`);
      });
      
      if (result.suggestions.length > 0) {
        console.log(`\n💡 Suggestions: ${result.suggestions.join(', ')}`);
      }
      
      console.log('\n🔗 URLs:');
      Object.entries(result.handles).forEach(([platform, handleInfo]) => {
        console.log(`   ${platform}: ${handleInfo.url}`);
      });
      
    } catch (error) {
      console.error(`❌ Error testing "${name}":`, error.message);
    }
  }

  console.log('\n✅ Social handle availability test completed!');
  console.log('\n📋 Expected Results:');
  console.log('   - Fathomly, Quillan, TestCompany12345: Should be mostly available');
  console.log('   - Apple, Microsoft, Google: Should be mostly taken');
  console.log('   - Unknown status is normal for some platforms due to rate limiting');
}

// Run the test
if (require.main === module) {
  testSocialHandles().catch(console.error);
}

module.exports = { testSocialHandles };
