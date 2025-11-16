#!/usr/bin/env node

/**
 * Test script for the Uniqueness Scoring functionality
 * Tests the new Google Custom Search API integration
 */

// Load environment variables
require('dotenv').config();

// Import the checkUniqueness function
const { checkUniqueness } = require('./name-vetting.js');

async function testUniqueness() {
  console.log('🧪 Testing Uniqueness Scoring Implementation\n');

  // Test cases
  const testNames = [
    'Fathomly',           // Should be very unique (from our DBA candidates)
    'Quillan',            // Should be very unique
    'Apple Inc',          // Should have many results
    'Microsoft',          // Should have many results
    'Veriquant',          // Should be unique (from our DBA candidates)
    'TestCompany12345'    // Should be very unique (random)
  ];

  for (const name of testNames) {
    console.log(`\n🔍 Testing: "${name}"`);
    console.log('─'.repeat(50));
    
    try {
      const result = await checkUniqueness(name);
      
      console.log(`📊 Result Count: ${result.resultCount || 'N/A'}`);
      console.log(`⭐ Uniqueness Score: ${result.uniquenessScore}/30`);
      console.log(`📝 Note: ${result.note}`);
      console.log(`🔗 Top Results: ${result.topResults.length} found`);
      
      if (result.conflicts.length > 0) {
        console.log(`⚠️  Conflicts: ${result.conflicts.length} potential conflicts`);
        result.conflicts.forEach(conflict => {
          console.log(`   - ${conflict.type}: ${conflict.title}`);
        });
      }
      
    } catch (error) {
      console.error(`❌ Error testing "${name}":`, error.message);
    }
  }

  console.log('\n✅ Uniqueness scoring test completed!');
}

// Run the test
if (require.main === module) {
  testUniqueness().catch(console.error);
}

module.exports = { testUniqueness };
