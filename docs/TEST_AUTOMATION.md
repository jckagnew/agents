# 🧪 Test Automation Guide

## Overview

The Software Factory includes comprehensive automated testing across unit, integration, and end-to-end (E2E) test suites to ensure code quality and reliability before deployment.

**Status**: ✅ Production Ready
**Last Updated**: October 2024

---

## Test Pyramid

```
        /\
       /E2E\      ← Fewer, slower, expensive (UI/Browser)
      /------\
     /  INT  \    ← Medium count, moderate speed (API/DB)
    /----------\
   /   UNIT    \  ← Many, fast, cheap (Functions/Logic)
  /--------------\
```

**Philosophy**: More unit tests, fewer integration tests, even fewer E2E tests.

---

## Tools

### Vitest
**Purpose**: Unit and Integration Testing
**Version**: 4.0.0+
**Coverage**: TypeScript/JavaScript utilities, business logic

**Why Vitest**:
- ⚡ Extremely fast (Vite-powered)
- 🔧 Jest-compatible API
- 📊 Built-in coverage
- 🎯 Watch mode for development

### Supertest
**Purpose**: HTTP/API Integration Testing
**Version**: 7.0.0+
**Coverage**: REST API endpoints, middleware

**Why Supertest**:
- 🌐 HTTP assertions
- 🔗 Works with Express/Next.js
- 📝 Readable test syntax

### Playwright
**Purpose**: End-to-End Testing
**Version**: 1.56.0+
**Coverage**: Full user flows, cross-browser testing

**Why Playwright**:
- 🎭 Multi-browser support (Chromium, Firefox, WebKit)
- 📱 Mobile viewport testing
- 📸 Screenshots and videos
- 🔍 Auto-wait for elements

---

## Installation

All dependencies are already in `package.json`. Just run:

```bash
npm install
```

**Playwright Browsers**:
```bash
npx playwright install
```

---

## Usage

### Quick Start

```bash
# Run all tests
npm run test:all

# Run specific test types
npm run test:unit
npm run test:integration
npm run test:e2e

# Watch mode (for development)
npm run test:watch

# Generate coverage reports
npm run test:coverage

# Strict mode (fail on any error)
npm run test:all:strict
```

### Manual Execution

```bash
# Unit tests with Vitest
npx vitest run tests/unit

# Integration tests
npx vitest run tests/integration

# E2E tests with Playwright
npx playwright test

# With specific browser
npx playwright test --project=chromium

# Headed mode (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

---

## Test Structure

```
tests/
├── unit/                    # Unit tests (Vitest)
│   ├── backlog-sync.test.js
│   ├── security-scan.test.js
│   └── ...
├── integration/             # Integration tests (Vitest + Supertest)
│   ├── api.test.js
│   └── database.test.js
└── e2e/                     # End-to-end tests (Playwright)
    ├── hydrotrack.spec.ts
    └── ...
```

---

## Unit Tests

### Purpose
Test individual functions, modules, and utilities in isolation.

### Characteristics
- ✅ Fast (< 1ms per test)
- ✅ No external dependencies
- ✅ Mocked dependencies
- ✅ High coverage (aim for 80%+)

### Example

```javascript
// tests/unit/backlog-sync.test.js
import { describe, it, expect } from 'vitest';

describe('Backlog Sync - Deduplication', () => {
  it('should remove duplicate items by title', () => {
    const items = [
      { title: 'Feature A', description: 'Test 1' },
      { title: 'Feature B', description: 'Test 2' },
      { title: 'Feature A', description: 'Duplicate' }
    ];

    const result = deduplicateItems(items);

    expect(result).toHaveLength(2);
    expect(result.map(i => i.title)).toEqual(['Feature A', 'Feature B']);
  });
});
```

### Best Practices
- ✅ One assertion per test (generally)
- ✅ Descriptive test names ("should X when Y")
- ✅ Arrange-Act-Assert pattern
- ✅ Mock external dependencies
- ❌ Don't test implementation details
- ❌ Don't test framework code

---

## Integration Tests

### Purpose
Test interactions between components, APIs, and databases.

### Characteristics
- ⚡ Moderate speed (< 100ms per test)
- 🔗 Real HTTP requests
- 🗄️ Test database (or mocked)
- 📊 Medium coverage (60-70%)

### Example

```javascript
// tests/integration/api.test.js
import { describe, it, expect } from 'vitest';
import request from 'supertest';
import app from '@/server';

describe('POST /api/entries', () => {
  it('should create a new entry', async () => {
    const newEntry = {
      value: 500,
      unit: 'ml',
      timestamp: '2025-10-24T12:00:00Z'
    };

    const response = await request(app)
      .post('/api/entries')
      .send(newEntry);

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.value).toBe(500);
  });

  it('should validate required fields', async () => {
    const invalidEntry = { unit: 'ml' }; // missing value

    const response = await request(app)
      .post('/api/entries')
      .send(invalidEntry);

    expect(response.status).toBe(400);
    expect(response.body.error).toContain('required');
  });
});
```

### Best Practices
- ✅ Test happy paths and error cases
- ✅ Test validation and error handling
- ✅ Use test database or mocks
- ✅ Clean up data after tests
- ❌ Don't test third-party APIs directly
- ❌ Don't rely on test execution order

---

## E2E Tests

### Purpose
Test complete user workflows from start to finish.

### Characteristics
- 🐢 Slower (1-10s per test)
- 🌐 Real browser interactions
- 📱 Multi-device/viewport
- 🎯 Critical paths only (20-30% coverage)

### Example

```typescript
// tests/e2e/hydrotrack.spec.ts
import { test, expect } from '@playwright/test';

test('should log water intake entry', async ({ page }) => {
  await page.goto('/dashboard');

  // Click "Log Entry" button
  await page.click('button:has-text("Log Entry")');

  // Enter water amount
  await page.fill('input[type="number"]', '500');

  // Submit entry
  await page.click('button:has-text("Save")');

  // Verify success
  await expect(page.locator('text=Entry logged successfully')).toBeVisible();
  await expect(page.locator('text=500 ml')).toBeVisible();
});

test('should be responsive on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/dashboard');

  // Bottom navigation should be visible
  const bottomNav = page.locator('[data-testid="bottom-nav"]');
  await expect(bottomNav).toBeVisible();
});
```

### Best Practices
- ✅ Test critical user journeys
- ✅ Test across browsers/devices
- ✅ Use data-testid attributes
- ✅ Test accessibility
- ❌ Don't test every edge case (that's for unit tests)
- ❌ Don't create brittle selectors

---

## Coverage Expectations

### Unit Tests
**Target**: 80-90% coverage
**Focus**: Business logic, utilities, helpers

### Integration Tests
**Target**: 60-70% coverage
**Focus**: API endpoints, middleware, database operations

### E2E Tests
**Target**: 20-30% coverage (of critical paths)
**Focus**: Happy paths, critical user flows

### Overall
**Target**: 70-80% total coverage
**Exclusions**: Config files, type definitions, generated code

---

## Test Reports

### Output Location
All reports saved to: `.claude/idea-to-design/test-reports/`

### Generated Files

**Unit/Integration Reports**:
- `unit-report.json` - Vitest unit test results
- `integration-report.json` - Vitest integration results
- `coverage/` - HTML coverage reports

**E2E Reports**:
- `e2e-report.json` - Playwright test results
- `playwright-report/` - HTML test report with screenshots
- `test-results/` - Screenshots/videos of failures

**Unified Summary**:
- `test-summary.md` - Aggregated results from all suites
- `test-results.json` - Combined JSON report

### Example Summary

```markdown
# Test Summary

**Generated**: 2025-10-24T12:00:00.000Z
**Total Tests**: 45

## Overview

| Test Type | Total | Passed | Failed | Skipped | Status |
|-----------|-------|--------|--------|---------|--------|
| Unit      | 25    | 25     | 0      | 0       | ✅ Passed |
| Integration| 12   | 12     | 0      | 0       | ✅ Passed |
| E2E       | 8     | 8      | 0      | 0       | ✅ Passed |
| **Total** | **45**| **45** | **0**  | **0**   | ✅ **Passed** |
```

---

## CI/CD Integration

### GitHub Actions

Tests run automatically in CI/CD pipeline after security scans.

**Workflow**: `.github/workflows/ci.yml`

```yaml
- name: Run unit tests
  run: npm run test:unit

- name: Run integration tests
  run: npm run test:integration

- name: Install Playwright browsers
  run: npx playwright install --with-deps

- name: Run E2E tests
  run: npm run test:e2e

- name: Upload test reports
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: .claude/idea-to-design/test-reports/
```

**Behavior**:
- Runs on all pushes and PRs
- Fails build if any tests fail
- Uploads reports as artifacts
- Generates coverage reports

### Pre-commit Hook

Add to `.husky/pre-commit` or `.pre-commit-config.yaml`:

```bash
#!/bin/sh
npm run test:unit
```

---

## Writing New Tests

### Unit Test Template

```javascript
// tests/unit/my-module.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { myFunction } from '@scripts/my-module';

describe('MyModule', () => {
  describe('myFunction', () => {
    it('should return expected result when given valid input', () => {
      // Arrange
      const input = 'test';

      // Act
      const result = myFunction(input);

      // Assert
      expect(result).toBe('expected');
    });

    it('should throw error when given invalid input', () => {
      expect(() => myFunction(null)).toThrow('Invalid input');
    });
  });
});
```

### Integration Test Template

```javascript
// tests/integration/my-api.test.js
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import app from '@/server';

describe('GET /api/resource', () => {
  beforeAll(async () => {
    // Setup: seed test database
  });

  afterAll(async () => {
    // Cleanup: clear test data
  });

  it('should return 200 and list of resources', async () => {
    const response = await request(app).get('/api/resource');

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('data');
    expect(Array.isArray(response.body.data)).toBe(true);
  });
});
```

### E2E Test Template

```typescript
// tests/e2e/my-feature.spec.ts
import { test, expect } from '@playwright/test';

test.describe('My Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should perform user action successfully', async ({ page }) => {
    // Navigate
    await page.goto('/feature');

    // Interact
    await page.click('button[data-testid="action-button"]');

    // Assert
    await expect(page.locator('text=Success')).toBeVisible();
  });
});
```

---

## Debugging Tests

### Unit/Integration Tests

```bash
# Run specific test file
npx vitest run tests/unit/backlog-sync.test.js

# Run tests matching pattern
npx vitest run -t "should deduplicate"

# Debug mode
npx vitest --inspect-brk

# UI mode
npx vitest --ui
```

### E2E Tests

```bash
# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode with Playwright Inspector
npx playwright test --debug

# Run specific test
npx playwright test tests/e2e/hydrotrack.spec.ts

# Trace viewer (after test run)
npx playwright show-trace trace.zip
```

---

## Troubleshooting

### Vitest Issues

**Error: Cannot find module**
```bash
# Check import paths
# Ensure aliases configured in vitest.config.ts
```

**Tests timeout**
```javascript
// Increase timeout for slow tests
it('slow test', async () => {
  // test code
}, { timeout: 10000 });
```

**Coverage not working**
```bash
# Install coverage provider
npm install -D @vitest/coverage-v8
```

### Playwright Issues

**Browsers not installed**
```bash
npx playwright install --with-deps
```

**Tests flaky**
```typescript
// Add explicit waits
await page.waitForLoadState('networkidle');
await expect(element).toBeVisible({ timeout: 10000 });
```

**Can't find element**
```typescript
// Use data-testid attributes
<button data-testid="submit-button">Submit</button>

await page.click('[data-testid="submit-button"]');
```

### General Issues

**Tests pass locally but fail in CI**
- Check environment variables
- Verify dependencies installed
- Check file permissions
- Review CI logs

**Tests are too slow**
- Run tests in parallel
- Use test.concurrent in Vitest
- Mock expensive operations
- Reduce E2E test count

---

## Best Practices

### General
- ✅ Write tests first (TDD)
- ✅ Keep tests simple and focused
- ✅ Use descriptive test names
- ✅ Follow Arrange-Act-Assert pattern
- ✅ Test behavior, not implementation
- ❌ Don't test framework code
- ❌ Don't create interdependent tests

### Performance
- ⚡ Run unit tests on every save
- ⚡ Run integration tests before commit
- ⚡ Run E2E tests before PR/deploy
- ⚡ Use test.concurrent for independent tests
- ⚡ Mock slow operations

### Maintainability
- 📝 Comment complex test setup
- 📝 Use test factories for fixtures
- 📝 DRY principle (helper functions)
- 📝 Keep tests close to source
- 📝 Update tests with code changes

---

## Coverage Reports

### Viewing Coverage

```bash
# Generate and view coverage
npm run test:coverage

# Open HTML report
open .claude/idea-to-design/test-reports/coverage/index.html
```

### Coverage Thresholds

Configure in `vitest.config.ts`:

```typescript
export default defineConfig({
  test: {
    coverage: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
});
```

---

## Integration with Backlog Sync

Failed tests can be tracked as backlog items:

```bash
# Run tests and capture failures
npm run test:all

# Sync failed tests to backlog
node scripts/backlog-sync.js --session-dir .claude/idea-to-design/test-reports
```

This creates issues like:
```json
{
  "title": "[Test] Unit test failure in backlog-sync.test.js",
  "priority": "P1",
  "labels": ["test-failure", "bug"],
  "source": "Test Automation"
}
```

---

## Resources

### Documentation
- [Vitest Docs](https://vitest.dev/)
- [Playwright Docs](https://playwright.dev/)
- [Supertest Docs](https://github.com/visionmedia/supertest)

### Testing Guides
- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

### Tools
- [Vitest UI](https://vitest.dev/guide/ui.html)
- [Playwright Inspector](https://playwright.dev/docs/debug)
- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)

---

## FAQ

**Q: How many tests should I write?**
A: Follow the test pyramid: Many unit tests, fewer integration tests, even fewer E2E tests.

**Q: Should I test private functions?**
A: No, test public API only. Private functions are tested indirectly through public methods.

**Q: How do I test async code?**
A: Use `async/await` syntax. Vitest and Playwright handle promises automatically.

**Q: What about snapshot testing?**
A: Use sparingly. Good for React components, bad for dynamic data.

**Q: How do I speed up tests?**
A: Run in parallel, mock expensive operations, use test databases, reduce E2E tests.

**Q: Should I test third-party libraries?**
A: No, assume they work. Test your integration with them.

---

**Last Updated**: October 2024
**Next Review**: January 2025
