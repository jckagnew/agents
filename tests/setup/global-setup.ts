import { chromium, FullConfig } from '@playwright/test'

async function globalSetup(config: FullConfig) {
  console.log('🌍 Starting global E2E test setup...')
  
  // Start browser for setup tasks
  const browser = await chromium.launch()
  const page = await browser.newPage()
  
  try {
    // Wait for the application to be ready
    const baseURL = config.projects[0].use?.baseURL || 'http://localhost:3000'
    console.log(`📡 Checking application at ${baseURL}...`)
    
    // Try to access the application
    const response = await page.goto(baseURL, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    })
    
    if (!response || !response.ok()) {
      throw new Error(`Application not ready at ${baseURL}. Status: ${response?.status()}`)
    }
    
    console.log('✅ Application is ready for testing')
    
    // Optional: Set up test data or perform authentication
    await setupTestData(page)
    
  } catch (error) {
    console.error('❌ Global setup failed:', error)
    throw error
  } finally {
    await browser.close()
  }
  
  console.log('🎉 Global E2E test setup complete')
}

async function setupTestData(page: any) {
  try {
    console.log('📊 Setting up test data...')
    
    // Create test user if needed
    await page.goto('/api/test/setup', { waitUntil: 'networkidle' })
    
    // Wait for setup to complete
    await page.waitForTimeout(2000)
    
    console.log('✅ Test data setup complete')
  } catch (error) {
    console.warn('⚠️  Test data setup failed (this may be expected):', error.message)
  }
}

export default globalSetup
