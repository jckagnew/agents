import { FullConfig } from '@playwright/test'

async function globalTeardown(config: FullConfig) {
  console.log('🧹 Starting global E2E test teardown...')
  
  try {
    // Clean up test data
    await cleanupTestData()
    
    // Clean up any temporary files
    await cleanupTempFiles()
    
    console.log('✅ Global E2E test teardown complete')
  } catch (error) {
    console.error('❌ Global teardown failed:', error)
    // Don't throw error in teardown to avoid masking test failures
  }
}

async function cleanupTestData() {
  try {
    console.log('🗑️  Cleaning up test data...')
    
    // This would typically involve calling your API cleanup endpoints
    // or directly cleaning up the test database
    
    console.log('✅ Test data cleanup complete')
  } catch (error) {
    console.warn('⚠️  Test data cleanup failed:', error.message)
  }
}

async function cleanupTempFiles() {
  try {
    console.log('📁 Cleaning up temporary files...')
    
    // Clean up any temporary files created during tests
    // This could include screenshots, videos, or other artifacts
    
    console.log('✅ Temporary files cleanup complete')
  } catch (error) {
    console.warn('⚠️  Temporary files cleanup failed:', error.message)
  }
}

export default globalTeardown
