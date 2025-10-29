import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest'
import { execSync } from 'child_process'
import { existsSync, mkdirSync, rmSync } from 'fs'
import { join } from 'path'

// Test database and server configuration
const TEST_DB_PATH = './test-db.sqlite'
const TEST_PORT = 3001
const TEST_BASE_URL = `http://localhost:${TEST_PORT}`

// Global test state
let testServer: any = null
let testDb: any = null

export const setupIntegrationTests = () => {
  beforeAll(async () => {
    console.log('🚀 Setting up integration test environment...')
    
    // Create test database
    if (existsSync(TEST_DB_PATH)) {
      rmSync(TEST_DB_PATH)
    }
    
    // Initialize test database schema
    try {
      execSync('npx prisma migrate dev --name test-setup', { 
        stdio: 'inherit',
        env: { ...process.env, DATABASE_URL: `file:${TEST_DB_PATH}` }
      })
    } catch (error) {
      console.warn('⚠️  Prisma migration failed, using SQLite directly')
    }
    
    // Start test server
    try {
      const { spawn } = await import('child_process')
      testServer = spawn('node', ['scripts/test-server.js'], {
        env: { 
          ...process.env, 
          PORT: TEST_PORT.toString(),
          DATABASE_URL: `file:${TEST_DB_PATH}`,
          NODE_ENV: 'test'
        },
        stdio: 'pipe'
      })
      
      // Wait for server to start
      await new Promise((resolve) => setTimeout(resolve, 2000))
      
      console.log(`✅ Test server started on ${TEST_BASE_URL}`)
    } catch (error) {
      console.error('❌ Failed to start test server:', error)
      throw error
    }
  })
  
  afterAll(async () => {
    console.log('🧹 Cleaning up integration test environment...')
    
    // Stop test server
    if (testServer) {
      testServer.kill()
      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
    
    // Clean up test database
    if (existsSync(TEST_DB_PATH)) {
      rmSync(TEST_DB_PATH)
    }
    
    console.log('✅ Integration test cleanup complete')
  })
  
  beforeEach(async () => {
    // Reset database state before each test
    if (existsSync(TEST_DB_PATH)) {
      // Clear test data
      try {
        execSync(`sqlite3 ${TEST_DB_PATH} "DELETE FROM users; DELETE FROM sessions; DELETE FROM weight_entries;"`, {
          stdio: 'pipe'
        })
      } catch (error) {
        console.warn('⚠️  Database cleanup failed:', error)
      }
    }
  })
  
  afterEach(async () => {
    // Additional cleanup after each test if needed
  })
}

// Export test configuration
export const testConfig = {
  baseUrl: TEST_BASE_URL,
  port: TEST_PORT,
  dbPath: TEST_DB_PATH,
  timeout: 10000
}

// Helper functions for integration tests
export const createTestUser = async (userData: any = {}) => {
  const defaultUser = {
    email: 'test@example.com',
    name: 'Test User',
    password: 'testpassword123',
    ...userData
  }
  
  // This would be implemented based on your API structure
  const response = await fetch(`${TEST_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(defaultUser)
  })
  
  if (!response.ok) {
    throw new Error(`Failed to create test user: ${response.statusText}`)
  }
  
  return response.json()
}

export const createTestWeightEntry = async (entryData: any = {}) => {
  const defaultEntry = {
    weight: 70.5,
    bodyFat: 15.0,
    date: new Date().toISOString(),
    notes: 'Test entry',
    ...entryData
  }
  
  const response = await fetch(`${TEST_BASE_URL}/api/weight-entries`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(defaultEntry)
  })
  
  if (!response.ok) {
    throw new Error(`Failed to create test weight entry: ${response.statusText}`)
  }
  
  return response.json()
}

export const cleanupTestData = async () => {
  // Clean up any test data created during tests
  try {
    await fetch(`${TEST_BASE_URL}/api/test/cleanup`, {
      method: 'POST'
    })
  } catch (error) {
    console.warn('⚠️  Test cleanup failed:', error)
  }
}
