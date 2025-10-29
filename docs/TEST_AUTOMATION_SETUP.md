# Test Automation Setup Guide

## Overview

This guide explains how to set up and run the comprehensive test automation suite for the Software Factory, including unit tests, integration tests, and end-to-end tests.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git repository with code to test
- Modern web browser (for E2E tests)

## Test Architecture

The test suite is organized into three layers:

### 1. Unit Tests (Vitest)
- **Purpose**: Test individual functions and components in isolation
- **Location**: `tests/unit/` and `src/**/*.{test,spec}.{js,ts}`
- **Framework**: Vitest with TypeScript support
- **Coverage**: 80% threshold for branches, functions, lines, and statements

### 2. Integration Tests (Supertest + Vitest)
- **Purpose**: Test API endpoints and database interactions
- **Location**: `tests/integration/`
- **Framework**: Supertest for HTTP testing, Vitest for test runner
- **Database**: SQLite test database with automatic cleanup

### 3. End-to-End Tests (Playwright)
- **Purpose**: Test complete user workflows in real browsers
- **Location**: `tests/e2e/`
- **Framework**: Playwright with multi-browser support
- **Browsers**: Chrome, Firefox, Safari, Edge, Mobile Chrome, Mobile Safari

## Installation

### 1. Install Dependencies

```bash
# Install test dependencies
npm install --save-dev vitest @vitest/ui supertest @types/supertest @playwright/test

# Install Playwright browsers
npx playwright install
```

### 2. Verify Installation

```bash
# Check Vitest installation
npx vitest --version

# Check Playwright installation
npx playwright --version

# Check Supertest installation
node -e "console.log(require('supertest/package.json').version)"
```

## Configuration Files

### 1. Vitest Configuration (`vitest.config.ts`)

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/unit/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  }
})
```

### 2. Playwright Configuration (`playwright.config.ts`)

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ['html', { outputFolder: 'reports/e2e-test-report' }],
    ['json', { outputFile: 'reports/e2e-test-results.json' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
})
```

### 3. Integration Test Setup (`tests/integration/setup.ts`)

```typescript
import { beforeAll, afterAll } from 'vitest'

export const setupIntegrationTests = () => {
  beforeAll(async () => {
    // Start test server
    // Initialize test database
  })
  
  afterAll(async () => {
    // Stop test server
    // Clean up test database
  })
}
```

## Folder Structure

```
tests/
├── unit/                    # Unit tests
│   ├── components/         # React component tests
│   ├── utils/              # Utility function tests
│   ├── services/           # Service layer tests
│   └── hooks/              # Custom hook tests
├── integration/            # Integration tests
│   ├── api/                # API endpoint tests
│   ├── database/           # Database interaction tests
│   └── setup.ts            # Integration test setup
├── e2e/                    # End-to-end tests
│   ├── auth/               # Authentication flows
│   ├── weight-tracking/    # Weight tracking workflows
│   ├── goals/              # Goal management flows
│   └── settings/           # Settings and preferences
└── setup/                  # Test setup files
    ├── unit-setup.ts       # Unit test setup
    ├── global-setup.ts     # E2E global setup
    ├── global-teardown.ts  # E2E global teardown
    └── test-server.js      # Test server for integration tests
```

## Running Tests

### 1. Unit Tests

```bash
# Run all unit tests
npm run test:unit

# Run unit tests in watch mode
npm run test:unit:watch

# Run unit tests with coverage
npm run test:unit:coverage

# Run specific test file
npm run test:unit -- tests/unit/components/WeightEntry.test.tsx
```

### 2. Integration Tests

```bash
# Run all integration tests
npm run test:integration

# Run integration tests in watch mode
npm run test:integration:watch

# Run specific integration test
npm run test:integration -- tests/integration/api/weight-entries.test.ts
```

### 3. End-to-End Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed

# Run E2E tests for specific browser
npm run test:e2e -- --project=chromium

# Run specific E2E test
npm run test:e2e -- tests/e2e/weight-tracking/entry-creation.spec.ts
```

### 4. All Tests

```bash
# Run all tests (unit + integration + e2e)
npm run test:all

# Run tests in CI mode
npm run test:ci
```

## Writing Tests

### 1. Unit Test Example

```typescript
// tests/unit/utils/weight-calculations.test.ts
import { describe, it, expect } from 'vitest'
import { calculateBMI, calculateBodyFatPercentage } from '@/utils/weight-calculations'

describe('Weight Calculations', () => {
  it('should calculate BMI correctly', () => {
    const weight = 70 // kg
    const height = 1.75 // m
    const bmi = calculateBMI(weight, height)
    
    expect(bmi).toBeCloseTo(22.86, 2)
  })
  
  it('should calculate body fat percentage correctly', () => {
    const weight = 70
    const bodyFat = 15
    const percentage = calculateBodyFatPercentage(weight, bodyFat)
    
    expect(percentage).toBe(15)
  })
})
```

### 2. Integration Test Example

```typescript
// tests/integration/api/weight-entries.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import request from 'supertest'
import { setupIntegrationTests, testConfig } from '../setup'

describe('Weight Entries API', () => {
  beforeAll(() => {
    setupIntegrationTests()
  })
  
  it('should create a new weight entry', async () => {
    const entryData = {
      weight: 70.5,
      bodyFat: 15.0,
      date: new Date().toISOString(),
      notes: 'Test entry'
    }
    
    const response = await request(testConfig.baseUrl)
      .post('/api/weight-entries')
      .send(entryData)
      .expect(201)
    
    expect(response.body).toMatchObject(entryData)
    expect(response.body.id).toBeDefined()
  })
  
  it('should get all weight entries', async () => {
    const response = await request(testConfig.baseUrl)
      .get('/api/weight-entries')
      .expect(200)
    
    expect(Array.isArray(response.body)).toBe(true)
  })
})
```

### 3. E2E Test Example

```typescript
// tests/e2e/weight-tracking/entry-creation.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Weight Entry Creation', () => {
  test('should create a new weight entry', async ({ page }) => {
    // Navigate to weight tracking page
    await page.goto('/weight-tracking')
    
    // Fill in weight entry form
    await page.fill('[data-testid="weight-input"]', '70.5')
    await page.fill('[data-testid="body-fat-input"]', '15.0')
    await page.fill('[data-testid="notes-input"]', 'Test entry')
    
    // Submit form
    await page.click('[data-testid="submit-button"]')
    
    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible()
    
    // Verify entry appears in list
    await expect(page.locator('[data-testid="weight-entry"]')).toContainText('70.5')
  })
  
  test('should validate required fields', async ({ page }) => {
    await page.goto('/weight-tracking')
    
    // Try to submit without filling required fields
    await page.click('[data-testid="submit-button"]')
    
    // Verify validation errors
    await expect(page.locator('[data-testid="weight-error"]')).toBeVisible()
    await expect(page.locator('[data-testid="body-fat-error"]')).toBeVisible()
  })
})
```

## Test Data Management

### 1. Mock Data Factories

```typescript
// tests/setup/unit-setup.ts
export const createMockUser = (overrides = {}) => ({
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date().toISOString(),
  ...overrides
})

export const createMockWeightEntry = (overrides = {}) => ({
  id: 'entry-123',
  userId: 'user-123',
  weight: 70.5,
  bodyFat: 15.0,
  date: new Date().toISOString(),
  ...overrides
})
```

### 2. Database Seeding

```typescript
// tests/setup/database-seed.ts
export const seedTestData = async () => {
  // Create test users
  // Create test weight entries
  // Create test goals
}
```

## CI/CD Integration

### 1. GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:unit:coverage
      
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:integration
      
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
```

## Best Practices

### 1. Test Organization
- Group related tests in describe blocks
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Keep tests independent and isolated

### 2. Test Data
- Use factories for creating test data
- Clean up test data after each test
- Use realistic but minimal test data
- Avoid hardcoded values in tests

### 3. Assertions
- Use specific assertions over generic ones
- Test both positive and negative cases
- Verify error conditions and edge cases
- Use meaningful assertion messages

### 4. Performance
- Keep unit tests fast (< 100ms each)
- Use mocks for external dependencies
- Avoid unnecessary setup/teardown
- Run tests in parallel when possible

## Troubleshooting

### Common Issues

#### 1. Test Timeouts
```bash
# Increase timeout in vitest.config.ts
testTimeout: 10000

# Or in individual tests
test('slow test', async () => {
  // test code
}, 30000)
```

#### 2. Playwright Browser Issues
```bash
# Reinstall browsers
npx playwright install --force

# Run with debug mode
npx playwright test --debug
```

#### 3. Database Connection Issues
```bash
# Check database URL
echo $DATABASE_URL

# Reset test database
rm test-db.sqlite
npm run test:integration
```

#### 4. Port Conflicts
```bash
# Check if port is in use
lsof -i :3000

# Kill process using port
kill -9 $(lsof -t -i:3000)
```

## Debugging Tests

### 1. Unit Tests
```bash
# Run with debug output
npm run test:unit -- --reporter=verbose

# Run specific test with debug
npm run test:unit -- --run tests/unit/specific-test.test.ts
```

### 2. Integration Tests
```bash
# Run with debug output
DEBUG=* npm run test:integration

# Run with test server logs
npm run test:integration -- --reporter=verbose
```

### 3. E2E Tests
```bash
# Run in headed mode
npm run test:e2e:headed

# Run with debug mode
npx playwright test --debug

# Run with trace
npx playwright test --trace=on
```

## Coverage Reports

### 1. View Coverage
```bash
# Generate coverage report
npm run test:unit:coverage

# Open coverage report
open coverage/unit/index.html
```

### 2. Coverage Thresholds
- **Branches**: 80%
- **Functions**: 80%
- **Lines**: 80%
- **Statements**: 80%

## Next Steps

1. **Write Tests**: Start with unit tests for core functionality
2. **Add Integration Tests**: Test API endpoints and database interactions
3. **Create E2E Tests**: Test complete user workflows
4. **Set Up CI/CD**: Automate test execution in GitHub Actions
5. **Monitor Coverage**: Ensure test coverage meets thresholds

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Use
