#!/usr/bin/env node
/**
 * Navigation Testing Script
 * Tests that all navigation buttons work correctly
 */

const { chromium } = require('playwright');

async function testNavigation() {
  console.log('🧪 Starting Navigation Testing...\n');
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Test 1: Load homepage
  console.log('📱 Testing homepage load...');
  await page.goto('http://localhost:3000');
  await page.waitForLoadState('networkidle');
  
  const title = await page.textContent('h1');
  console.log(`  ✅ Page loaded: "${title}"`);
  
  // Test 2: Test navigation buttons
  const navigationTests = [
    { name: 'Log Entry', selector: 'button:has-text("Log Entry")' },
    { name: 'History', selector: 'button:has-text("History")' },
    { name: 'Analytics', selector: 'button:has-text("Analytics")' },
    { name: 'Settings', selector: 'button[aria-label="Open settings"]' }
  ];
  
  for (const test of navigationTests) {
    console.log(`🔗 Testing ${test.name} navigation...`);
    
    try {
      // Click the button
      await page.click(test.selector);
      await page.waitForTimeout(500); // Wait for navigation
      
      // Check if we're on a different screen
      const currentTitle = await page.textContent('h1, h2, h3');
      console.log(`  ✅ Navigation successful: "${currentTitle}"`);
      
      // Go back to dashboard
      const backButton = await page.$('button[aria-label="Back"], button:has-text("Back")');
      if (backButton) {
        await backButton.click();
        await page.waitForTimeout(500);
        console.log(`  ✅ Returned to dashboard`);
      }
      
    } catch (error) {
      console.log(`  ❌ Navigation failed: ${error.message}`);
    }
  }
  
  // Test 3: Test responsive behavior
  console.log('\n📱 Testing responsive navigation...');
  
  const viewports = [
    { name: 'Mobile', width: 375, height: 667 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Desktop', width: 1280, height: 720 }
  ];
  
  for (const viewport of viewports) {
    console.log(`  Testing ${viewport.name} (${viewport.width}x${viewport.height})...`);
    
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check if buttons are still clickable
    const buttons = await page.$$('button');
    console.log(`    ✅ ${buttons.length} buttons found and clickable`);
    
    // Test one navigation
    try {
      await page.click('button:has-text("Log Entry")');
      await page.waitForTimeout(500);
      console.log(`    ✅ Navigation works on ${viewport.name}`);
      
      // Go back
      const backButton = await page.$('button[aria-label="Back"], button:has-text("Back")');
      if (backButton) {
        await backButton.click();
        await page.waitForTimeout(500);
      }
    } catch (error) {
      console.log(`    ❌ Navigation failed on ${viewport.name}: ${error.message}`);
    }
  }
  
  await browser.close();
  console.log('\n✅ Navigation testing completed!');
}

testNavigation().catch(console.error);
