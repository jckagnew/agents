#!/usr/bin/env node
/**
 * Responsive Design Testing Script
 * Tests the weight tracker app across different viewport sizes
 */

const { chromium } = require('playwright');

const viewports = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Mobile Landscape', width: 667, height: 375 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Tablet Landscape', width: 1024, height: 768 },
  { name: 'Desktop', width: 1280, height: 720 },
  { name: 'Large Desktop', width: 1920, height: 1080 }
];

async function testResponsive() {
  console.log('🧪 Starting Responsive Design Testing...\n');
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  for (const viewport of viewports) {
    console.log(`📱 Testing ${viewport.name} (${viewport.width}x${viewport.height})`);
    
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto('http://localhost:3000');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Take screenshot
    const screenshot = await page.screenshot({ 
      fullPage: true,
      path: `test-results/responsive-${viewport.name.toLowerCase().replace(' ', '-')}.png`
    });
    
    // Test key elements are visible
    const title = await page.textContent('h1');
    const summaryCard = await page.$('.card-surface--summary, [class*="card-surface"]');
    const buttons = await page.$$('button');
    
    console.log(`  ✅ Title: "${title}"`);
    console.log(`  ✅ Summary card: ${summaryCard ? 'Found' : 'Missing'}`);
    console.log(`  ✅ Buttons: ${buttons.length} found`);
    
    // Test typography scaling
    const titleStyle = await page.evaluate(() => {
      const title = document.querySelector('h1');
      return title ? {
        fontSize: getComputedStyle(title).fontSize,
        fontFamily: getComputedStyle(title).fontFamily
      } : null;
    });
    
    if (titleStyle) {
      console.log(`  ✅ Typography: ${titleStyle.fontSize} ${titleStyle.fontFamily}`);
    }
    
    // Test responsive grid
    const gridItems = await page.$$('[class*="grid"]');
    console.log(`  ✅ Grid items: ${gridItems.length} found`);
    
    console.log(`  📸 Screenshot saved: test-results/responsive-${viewport.name.toLowerCase().replace(' ', '-')}.png\n`);
  }
  
  await browser.close();
  console.log('✅ Responsive testing completed!');
  console.log('📁 Check test-results/ directory for screenshots');
}

// Create test results directory
const fs = require('fs');
if (!fs.existsSync('test-results')) {
  fs.mkdirSync('test-results');
}

testResponsive().catch(console.error);
