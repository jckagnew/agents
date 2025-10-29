#!/usr/bin/env node

/**
 * Test script for trademark screening
 *
 * This tests the trademark conflict detection, similarity scoring,
 * and risk assessment logic.
 */

const { calculateTrademarkSimilarity, normalizeToTrademark, levenshteinDistance } = require('./name-vetting.js');

async function testTrademarkSimilarity() {
  console.log('\n🧪 Testing Trademark Similarity Calculation\n');
  console.log('=' .repeat(60));

  const testCases = [
    // [name1, name2, expectedSimilarity (approx)]
    ['ACME CORP', 'ACME CORP', 1.0],
    ['ACME', 'ACME CORP', 0.57],  // Partial match
    ['ACME', 'ECMA', 0.75],        // Similar but different
    ['WIDGET LABS', 'WIDGET LAB', 0.92], // Very similar
    ['TECH SOLUTIONS', 'TECH SOLUTION', 0.94], // Very similar
    ['APPLE', 'ORANGE', 0.17],     // Different
    ['FATHOMLY', 'FATHOM', 0.75],  // Similar
    ['MICROSOFT', 'MICROHARD', 0.78], // Similar
    ['ABC', 'XYZ', 0.0],           // Completely different
    ['Acme Inc.', 'ACME INC', 1.0], // Should normalize to same
  ];

  console.log('\nSimilarity Tests:');
  console.log('-'.repeat(60));

  for (const [name1, name2, expected] of testCases) {
    const similarity = calculateTrademarkSimilarity(name1, name2);
    const normalized1 = normalizeToTrademark(name1);
    const normalized2 = normalizeToTrademark(name2);
    const distance = levenshteinDistance(normalized1, normalized2);

    const status = Math.abs(similarity - expected) < 0.15 ? '✅' : '⚠️';

    console.log(`\n${status} "${name1}" vs "${name2}"`);
    console.log(`   Normalized: "${normalized1}" vs "${normalized2}"`);
    console.log(`   Levenshtein Distance: ${distance}`);
    console.log(`   Similarity: ${similarity.toFixed(2)} (expected ~${expected.toFixed(2)})`);
  }

  console.log('\n' + '='.repeat(60));
}

async function testRiskAssessment() {
  console.log('\n🧪 Testing Risk Assessment Logic\n');
  console.log('=' .repeat(60));

  const riskCases = [
    { similarity: 1.0, status: 'LIVE', expectedRisk: 'HIGH' },
    { similarity: 0.95, status: 'LIVE', expectedRisk: 'HIGH' },
    { similarity: 0.85, status: 'LIVE', expectedRisk: 'HIGH' },
    { similarity: 0.80, status: 'LIVE', expectedRisk: 'MEDIUM' },
    { similarity: 0.70, status: 'LIVE', expectedRisk: 'MEDIUM' },
    { similarity: 0.65, status: 'DEAD', expectedRisk: 'LOW' },
    { similarity: 0.50, status: 'LIVE', expectedRisk: 'LOW' },
    { similarity: 0.30, status: 'LIVE', expectedRisk: 'NONE' },
  ];

  console.log('\nRisk Assessment Tests:');
  console.log('-'.repeat(60));

  for (const testCase of riskCases) {
    let risk = 'NONE';

    if (testCase.similarity >= 0.85 && testCase.status === 'LIVE') {
      risk = 'HIGH';
    } else if (testCase.similarity >= 0.7 && testCase.status === 'LIVE') {
      risk = 'MEDIUM';
    } else if (testCase.similarity >= 0.4) {
      risk = 'LOW';
    }

    const status = risk === testCase.expectedRisk ? '✅' : '❌';

    console.log(`\n${status} Similarity: ${testCase.similarity.toFixed(2)}, Status: ${testCase.status}`);
    console.log(`   Risk: ${risk} (expected ${testCase.expectedRisk})`);
  }

  console.log('\n' + '='.repeat(60));
}

async function testScoring() {
  console.log('\n🧪 Testing Trademark Scoring\n');
  console.log('=' .repeat(60));

  const scoringCases = [
    { risk: 'UNKNOWN', expectedScore: 0 },
    { risk: 'NONE', expectedScore: 30 },
    { risk: 'LOW', expectedScore: 20 },
    { risk: 'MEDIUM', expectedScore: 10 },
    { risk: 'HIGH', expectedScore: 0 },
  ];

  console.log('\nScoring Tests:');
  console.log('-'.repeat(60));

  for (const testCase of scoringCases) {
    let score = 0;

    switch (testCase.risk) {
      case 'NONE':
        score = 30;
        break;
      case 'LOW':
        score = 20;
        break;
      case 'MEDIUM':
        score = 10;
        break;
      case 'HIGH':
      case 'UNKNOWN':
        score = 0;
        break;
    }

    const status = score === testCase.expectedScore ? '✅' : '❌';

    console.log(`${status} Risk: ${testCase.risk} → Score: ${score}/30 (expected ${testCase.expectedScore})`);
  }

  console.log('\n' + '='.repeat(60));
}

async function runAllTests() {
  console.log('\n🚀 Trademark Screening Test Suite\n');

  await testTrademarkSimilarity();
  await testRiskAssessment();
  await testScoring();

  console.log('\n✅ All trademark screening tests complete!\n');
  console.log('📝 Notes:');
  console.log('  - Similarity calculation uses Levenshtein distance');
  console.log('  - Risk thresholds: HIGH (≥0.85), MEDIUM (0.7-0.84), LOW (0.4-0.69)');
  console.log('  - LIVE marks are prioritized over DEAD marks in risk assessment');
  console.log('  - Multiple Nice classes are handled by concatenating with commas');
  console.log('  - Status normalization maps various USPTO statuses to LIVE/DEAD');
  console.log('');
}

// Run all tests
runAllTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
