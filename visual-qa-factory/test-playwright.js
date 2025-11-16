const { chromium } = require('playwright');

async function runVisualQA() {
    console.log('🎨 Starting Visual QA Review...');
    const startTime = Date.now();
    
    try {
        // Launch browser with system Chrome
        const browser = await chromium.launch({ 
            headless: true,
            executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        });
        const context = await browser.newContext();
        
        // Test different viewports
        const viewports = [
            { name: 'Desktop', width: 1440, height: 900 },
            { name: 'Tablet', width: 768, height: 1024 },
            { name: 'Mobile', width: 375, height: 667 }
        ];
        
        const results = [];
        
        for (const viewport of viewports) {
            console.log(`📱 Testing ${viewport.name} (${viewport.width}x${viewport.height})`);
            
            const page = await context.newPage();
            await page.setViewportSize({ width: viewport.width, height: viewport.height });
            
            // Navigate to the test page
            await page.goto('http://localhost:3000');
            
            // Wait for content to load
            await page.waitForLoadState('networkidle');
            
            // Take screenshot
            const screenshot = await page.screenshot({ 
                path: `screenshots/${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`,
                fullPage: true 
            });
            
            // Basic checks
            const title = await page.title();
            const h1Text = await page.textContent('h1');
            const buttonExists = await page.locator('.cta-button').isVisible();
            const hasErrors = await page.evaluate(() => {
                return window.console.error && window.console.error.length > 0;
            });
            
            results.push({
                viewport: viewport.name,
                title,
                h1Text,
                buttonExists,
                hasErrors,
                screenshot: `screenshots/${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`
            });
            
            await page.close();
        }
        
        await browser.close();
        
        const endTime = Date.now();
        const duration = (endTime - startTime) / 1000;
        
        // Generate quality score
        let score = 100;
        const issues = [];
        
        // Check title
        if (!results[0].title.includes('Visual QA Factory')) {
            score -= 10;
            issues.push('Page title not descriptive enough');
        }
        
        // Check H1
        if (!results[0].h1Text.includes('Visual QA Factory')) {
            score -= 15;
            issues.push('H1 heading not clear or missing');
        }
        
        // Check CTA button
        if (!results[0].buttonExists) {
            score -= 20;
            issues.push('Primary CTA button missing');
        }
        
        // Check responsive design
        const mobileH1 = results.find(r => r.viewport === 'Mobile')?.h1Text;
        if (mobileH1 && mobileH1.length < 10) {
            score -= 10;
            issues.push('Mobile H1 text too short');
        }
        
        // Check for errors
        const hasAnyErrors = results.some(r => r.hasErrors);
        if (hasAnyErrors) {
            score -= 15;
            issues.push('Console errors detected');
        }
        
        // Generate report
        console.log('\n📊 Visual QA Report');
        console.log('==================');
        console.log(`Overall Score: ${score}/100`);
        console.log(`Grade: ${score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : 'F'}`);
        console.log(`Duration: ${duration.toFixed(2)}s`);
        
        if (issues.length > 0) {
            console.log('\n🚨 Issues Found:');
            issues.forEach(issue => console.log(`- ${issue}`));
        } else {
            console.log('\n✅ No critical issues found');
        }
        
        console.log('\n📱 Viewport Results:');
        results.forEach(result => {
            console.log(`${result.viewport}: ${result.title} - H1: "${result.h1Text}" - Button: ${result.buttonExists ? '✅' : '❌'}`);
        });
        
        console.log('\n📸 Screenshots saved to screenshots/ directory');
        
        return { score, issues, duration, results };
        
    } catch (error) {
        console.error('❌ Error during Visual QA:', error.message);
        return { score: 0, issues: ['Test failed'], duration: 0, results: [] };
    }
}

// Create screenshots directory
const fs = require('fs');
if (!fs.existsSync('screenshots')) {
    fs.mkdirSync('screenshots');
}

// Run the test
runVisualQA().then(result => {
    console.log('\n🎯 Phase 1 Results Summary:');
    console.log(`Quality Score: ${result.score}/100`);
    console.log(`Time Taken: ${result.duration.toFixed(2)}s`);
    console.log(`Issues: ${result.issues.length}`);
    console.log(`Status: ${result.score >= 85 ? '✅ PASS' : '❌ FAIL'}`);
    
    if (result.score < 85) {
        console.log('\n🔄 Iteration needed - score below 85 threshold');
    } else {
        console.log('\n🎉 Phase 1 Success - ready for Phase 2!');
    }
});
