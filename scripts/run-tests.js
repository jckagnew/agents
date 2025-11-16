#!/usr/bin/env node

/**
 * Test Runner Script
 *
 * Purpose: Run all test suites (unit, integration, e2e) and generate comprehensive reports
 * Integrates with Software Factory pipeline for automated testing.
 *
 * Usage:
 *   node scripts/run-tests.js --type all
 *   node scripts/run-tests.js --type unit
 *   node scripts/run-tests.js --type integration
 *   node scripts/run-tests.js --type e2e
 *   node scripts/run-tests.js --type all --fail-on-error
 *
 * Features:
 * - Runs unit tests (Vitest)
 * - Runs integration tests (Vitest + Supertest)
 * - Runs E2E tests (Playwright)
 * - Generates unified test report
 * - Supports fail-fast mode for CI/CD
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================================
// CLI ARGUMENT PARSING
// ============================================================================

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index !== -1 && args[index + 1] ? args[index + 1] : null;
};

const testType = getArg('--type') || 'all';
const sessionDir = getArg('--session-dir') || '.claude/idea-to-design/test-reports';
const failOnError = args.includes('--fail-on-error');

console.log('🧪 Test Runner');
console.log(`   Type: ${testType}`);
console.log(`   Session: ${sessionDir}`);
console.log(`   Fail on Error: ${failOnError ? 'Yes' : 'No'}\n`);

// Ensure output directory exists
if (!fs.existsSync(sessionDir)) {
  fs.mkdirSync(sessionDir, { recursive: true });
}

// ============================================================================
// TEST EXECUTION
// ============================================================================

const results = {
  unit: null,
  integration: null,
  e2e: null,
  timestamp: new Date().toISOString()
};

/**
 * Run unit tests with Vitest
 */
function runUnitTests() {
  console.log('🔬 Running unit tests...\n');

  try {
    const output = execSync('npx vitest run --reporter=json --reporter=verbose', {
      encoding: 'utf8',
      stdio: 'pipe'
    });

    console.log('✅ Unit tests passed\n');

    return {
      status: 'passed',
      passed: true,
      output: output
    };
  } catch (error) {
    console.error('❌ Unit tests failed\n');
    console.error(error.stdout || error.message);

    return {
      status: 'failed',
      passed: false,
      error: error.message,
      output: error.stdout
    };
  }
}

/**
 * Run integration tests with Vitest
 */
function runIntegrationTests() {
  console.log('🔗 Running integration tests...\n');

  try {
    const output = execSync('npx vitest run tests/integration --reporter=json --reporter=verbose', {
      encoding: 'utf8',
      stdio: 'pipe'
    });

    console.log('✅ Integration tests passed\n');

    return {
      status: 'passed',
      passed: true,
      output: output
    };
  } catch (error) {
    console.error('❌ Integration tests failed\n');
    console.error(error.stdout || error.message);

    return {
      status: 'failed',
      passed: false,
      error: error.message,
      output: error.stdout
    };
  }
}

/**
 * Run E2E tests with Playwright
 */
function runE2ETests() {
  console.log('🎭 Running E2E tests...\n');

  try {
    const output = execSync('npx playwright test --reporter=json', {
      encoding: 'utf8',
      stdio: 'pipe'
    });

    console.log('✅ E2E tests passed\n');

    return {
      status: 'passed',
      passed: true,
      output: output
    };
  } catch (error) {
    console.error('❌ E2E tests failed\n');
    console.error(error.stdout || error.message);

    return {
      status: 'failed',
      passed: false,
      error: error.message,
      output: error.stdout
    };
  }
}

// ============================================================================
// REPORT GENERATION
// ============================================================================

/**
 * Parse test results from JSON output
 */
function parseResults(result) {
  if (!result || !result.output) {
    return { total: 0, passed: 0, failed: 0, skipped: 0 };
  }

  try {
    // Try to parse JSON from output
    const lines = result.output.split('\n');
    const jsonLine = lines.find(line => line.trim().startsWith('{'));

    if (jsonLine) {
      const data = JSON.parse(jsonLine);
      return {
        total: data.numTotalTests || 0,
        passed: data.numPassedTests || 0,
        failed: data.numFailedTests || 0,
        skipped: data.numPendingTests || 0
      };
    }
  } catch (error) {
    // Fallback to manual parsing or default
  }

  return {
    total: result.passed ? 1 : 0,
    passed: result.passed ? 1 : 0,
    failed: result.passed ? 0 : 1,
    skipped: 0
  };
}

/**
 * Generate unified test summary
 */
function generateTestSummary(results) {
  const timestamp = new Date().toISOString();

  const unitStats = parseResults(results.unit);
  const integrationStats = parseResults(results.integration);
  const e2eStats = parseResults(results.e2e);

  const totalTests = unitStats.total + integrationStats.total + e2eStats.total;
  const totalPassed = unitStats.passed + integrationStats.passed + e2eStats.passed;
  const totalFailed = unitStats.failed + integrationStats.failed + e2eStats.failed;
  const totalSkipped = unitStats.skipped + integrationStats.skipped + e2eStats.skipped;

  let summary = `# Test Summary

**Generated**: ${timestamp}
**Total Tests**: ${totalTests}

---

## Overview

| Test Type | Total | Passed | Failed | Skipped | Status |
|-----------|-------|--------|--------|---------|--------|
| **Unit** | ${unitStats.total} | ${unitStats.passed} | ${unitStats.failed} | ${unitStats.skipped} | ${results.unit?.passed ? '✅ Passed' : '❌ Failed'} |
| **Integration** | ${integrationStats.total} | ${integrationStats.passed} | ${integrationStats.failed} | ${integrationStats.skipped} | ${results.integration?.passed ? '✅ Passed' : '❌ Failed'} |
| **E2E** | ${e2eStats.total} | ${e2eStats.passed} | ${e2eStats.failed} | ${e2eStats.skipped} | ${results.e2e?.passed ? '✅ Passed' : '❌ Failed'} |
| **Total** | **${totalTests}** | **${totalPassed}** | **${totalFailed}** | **${totalSkipped}** | ${totalFailed === 0 ? '✅ **Passed**' : '❌ **Failed**'} |

---

## Test Results

`;

  if (results.unit) {
    summary += `### Unit Tests

**Status**: ${results.unit.passed ? '✅ Passed' : '❌ Failed'}
**Tests**: ${unitStats.total} total, ${unitStats.passed} passed, ${unitStats.failed} failed

`;
    if (!results.unit.passed) {
      summary += `**Error**:
\`\`\`
${results.unit.error || 'Test failures detected'}
\`\`\`

`;
    }
  }

  if (results.integration) {
    summary += `### Integration Tests

**Status**: ${results.integration.passed ? '✅ Passed' : '❌ Failed'}
**Tests**: ${integrationStats.total} total, ${integrationStats.passed} passed, ${integrationStats.failed} failed

`;
    if (!results.integration.passed) {
      summary += `**Error**:
\`\`\`
${results.integration.error || 'Test failures detected'}
\`\`\`

`;
    }
  }

  if (results.e2e) {
    summary += `### E2E Tests

**Status**: ${results.e2e.passed ? '✅ Passed' : '❌ Failed'}
**Tests**: ${e2eStats.total} total, ${e2eStats.passed} passed, ${e2eStats.failed} failed

`;
    if (!results.e2e.passed) {
      summary += `**Error**:
\`\`\`
${results.e2e.error || 'Test failures detected'}
\`\`\`

`;
    }
  }

  summary += `---

## Coverage

Coverage reports are available in:
- Unit: \`.claude/idea-to-design/test-reports/coverage/\`
- E2E: \`.claude/idea-to-design/test-reports/playwright-report/\`

---

## Next Steps

`;

  if (totalFailed > 0) {
    summary += `1. Review failed tests above
2. Fix failing test cases
3. Re-run tests: \`npm run test:all\`
4. Ensure all tests pass before deployment

**Failed Tests**: ${totalFailed}
`;
  } else {
    summary += `✅ All tests passed! Ready for deployment.

**Test Coverage**: ${totalTests} tests across ${[results.unit, results.integration, results.e2e].filter(Boolean).length} suites
`;
  }

  return summary;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  console.log('🚀 Starting test execution...\n');

  // Run tests based on type
  if (testType === 'all' || testType === 'unit') {
    results.unit = runUnitTests();
  }

  if (testType === 'all' || testType === 'integration') {
    results.integration = runIntegrationTests();
  }

  if (testType === 'all' || testType === 'e2e') {
    results.e2e = runE2ETests();
  }

  // Generate summary
  console.log('📝 Generating test summary...\n');
  const summary = generateTestSummary(results);

  const summaryPath = path.join(sessionDir, 'test-summary.md');
  fs.writeFileSync(summaryPath, summary);

  console.log(`✅ Test summary: ${summaryPath}\n`);

  // Save detailed results
  const resultsPath = path.join(sessionDir, 'test-results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));

  console.log(`✅ Test results: ${resultsPath}\n`);

  // Print summary
  console.log('='.repeat(60));
  console.log('📊 Test Execution Summary');
  console.log('='.repeat(60));

  if (results.unit) {
    console.log(`Unit Tests:        ${results.unit.passed ? '✅ Passed' : '❌ Failed'}`);
  }
  if (results.integration) {
    console.log(`Integration Tests: ${results.integration.passed ? '✅ Passed' : '❌ Failed'}`);
  }
  if (results.e2e) {
    console.log(`E2E Tests:         ${results.e2e.passed ? '✅ Passed' : '❌ Failed'}`);
  }

  console.log('='.repeat(60));

  // Fail build if requested and tests failed
  const allPassed = [results.unit, results.integration, results.e2e]
    .filter(Boolean)
    .every(r => r.passed);

  if (failOnError && !allPassed) {
    console.error('\n❌ Build failed: Test failures detected');
    console.error(`   Review: ${summaryPath}`);
    process.exit(1);
  }

  if (!allPassed) {
    console.warn('\n⚠️  Some tests failed');
    console.warn(`   Review: ${summaryPath}`);
    process.exit(1);
  } else {
    console.log('\n✅ All tests passed!');
  }
}

// Run main function
main().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
