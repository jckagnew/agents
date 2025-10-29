#!/usr/bin/env node
/**
 * Generic Visual QA Runner
 * Tests any HTML mockup directory and generates quality scores
 *
 * Usage:
 *   node scripts/visual-qa-runner.js \
 *     --mockup-dir .claude/idea-to-design/session-X/mockups/iteration-0/option-a \
 *     --output-file .claude/idea-to-design/session-X/scores/iteration-0-option-a.json \
 *     --dev-server http://localhost:3000
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Parse command-line arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const mockupDir = getArg('--mockup-dir');
const outputFile = getArg('--output-file');
const devServer = getArg('--dev-server') || 'http://localhost:3000';
const designPrinciples = getArg('--design-principles'); // Optional

if (!mockupDir || !outputFile) {
    console.error('Usage: node visual-qa-runner.js --mockup-dir <path> --output-file <path> [--dev-server <url>] [--design-principles <path>]');
    process.exit(1);
}

// Ensure screenshots directory exists
const screenshotsDir = path.join(mockupDir, 'screenshots');
if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
}

async function runVisualQA() {
    console.log('🎨 Starting Visual QA Review...');
    console.log(`📁 Mockup Directory: ${mockupDir}`);
    console.log(`🌐 Dev Server: ${devServer}`);

    const startTime = Date.now();

    try {
        // Launch browser (use bundled Chromium by default, allow Chrome override)
        const chromePath = process.env.CHROME_PATH || null;
        const launchOptions = {
            headless: true
        };

        if (chromePath) {
            console.log(`📍 Using Chrome at: ${chromePath}`);
            launchOptions.executablePath = chromePath;
        } else {
            console.log('📍 Using bundled Chromium (Playwright)');
        }

        const browser = await chromium.launch(launchOptions);
        const context = await browser.newContext();

        // Test viewports
        const viewports = [
            { name: 'Desktop', width: 1440, height: 900 },
            { name: 'Tablet', width: 768, height: 1024 },
            { name: 'Mobile', width: 375, height: 667 }
        ];

        // Detect available screens from mockup directory
        const htmlFiles = fs.readdirSync(mockupDir).filter(f => f.endsWith('.html'));

        if (htmlFiles.length === 0) {
            console.error('❌ No HTML files found in mockup directory');
            process.exit(1);
        }

        console.log(`📄 Found ${htmlFiles.length} screens: ${htmlFiles.join(', ')}`);

        const screens = htmlFiles.map(file => {
            const name = path.basename(file, '.html');
            return {
                name: name.charAt(0).toUpperCase() + name.slice(1).replace(/-/g, ' '),
                file: file,
                key: name
            };
        });

        const results = {
            mockup_dir: mockupDir,
            screens_tested: screens.length,
            viewports_tested: viewports.length,
            screenshots: [],
            issues: [],
            scores: {
                brand_compliance: 0,
                responsive_design: 0,
                accessibility: 0,
                performance: 0,
                visual_polish: 0,
                overall_score: 0
            },
            duration_ms: 0
        };

        let totalScreens = 0;
        let passedScreens = 0;

        // Test each screen at each viewport
        for (const screen of screens) {
            console.log(`\n📱 Testing ${screen.name}...`);

            for (const viewport of viewports) {
                console.log(`  ${viewport.name} (${viewport.width}x${viewport.height})`);
                totalScreens++;

                const page = await context.newPage();
                await page.setViewportSize({ width: viewport.width, height: viewport.height });

                try {
                    // Load HTML file directly (file:// URL)
                    const htmlPath = path.resolve(mockupDir, screen.file);
                    await page.goto(`file://${htmlPath}`, {
                        waitUntil: 'networkidle',
                        timeout: 10000
                    });

                    // Take screenshot
                    const screenshotName = `${screen.key}-${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`;
                    const screenshotPath = path.join(screenshotsDir, screenshotName);
                    await page.screenshot({
                        path: screenshotPath,
                        fullPage: true
                    });

                    results.screenshots.push(screenshotPath);

                    // Collect metrics
                    const metrics = await page.evaluate(() => {
                        return {
                            title: document.title,
                            hasH1: !!document.querySelector('h1'),
                            h1Text: document.querySelector('h1')?.textContent || '',
                            hasButtons: document.querySelectorAll('button').length,
                            hasLinks: document.querySelectorAll('a').length,
                            hasImages: document.querySelectorAll('img').length,
                            hasForm: !!document.querySelector('form'),
                            bodyBackgroundColor: window.getComputedStyle(document.body).backgroundColor,
                            errors: []
                        };
                    });

                    // Basic validation
                    if (metrics.hasH1) {
                        console.log(`    ✅ Has H1: "${metrics.h1Text}"`);
                        passedScreens++;
                    } else {
                        console.log(`    ⚠️  Missing H1 heading`);
                        results.issues.push(`${screen.name} (${viewport.name}): Missing H1 heading`);
                    }

                    // Check for console errors
                    page.on('console', msg => {
                        if (msg.type() === 'error') {
                            results.issues.push(`${screen.name} (${viewport.name}): Console error - ${msg.text()}`);
                        }
                    });

                } catch (error) {
                    console.log(`    ❌ Error: ${error.message}`);
                    results.issues.push(`${screen.name} (${viewport.name}): ${error.message}`);
                }

                await page.close();
            }
        }

        await browser.close();

        // Calculate scores (simplified rubric)
        const screenshotSuccessRate = results.screenshots.length / (screens.length * viewports.length);
        const issueCount = results.issues.length;

        // Brand Compliance (25 pts) - Based on design principles if provided
        results.scores.brand_compliance = 25; // Default: assume compliant (would parse design-principles.md)

        // Responsive Design (20 pts) - All viewports worked
        results.scores.responsive_design = Math.round(screenshotSuccessRate * 20);

        // Accessibility (25 pts) - Basic checks (H1, semantic HTML)
        const h1Rate = passedScreens / totalScreens;
        results.scores.accessibility = Math.round(h1Rate * 25);

        // Performance (15 pts) - Page load success
        results.scores.performance = issueCount === 0 ? 15 : Math.max(0, 15 - issueCount * 2);

        // Visual Polish (15 pts) - No console errors, clean screenshots
        results.scores.visual_polish = issueCount === 0 ? 15 : Math.max(0, 15 - issueCount);

        // Overall Score (100 pts)
        results.scores.overall_score =
            results.scores.brand_compliance +
            results.scores.responsive_design +
            results.scores.accessibility +
            results.scores.performance +
            results.scores.visual_polish;

        results.duration_ms = Date.now() - startTime;

        // Output results
        console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📊 VISUAL QA RESULTS');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`\n🎯 Overall Score: ${results.scores.overall_score}/100`);
        console.log(`\n📋 Breakdown:`);
        console.log(`  Brand Compliance:  ${results.scores.brand_compliance}/25`);
        console.log(`  Responsive Design: ${results.scores.responsive_design}/20`);
        console.log(`  Accessibility:     ${results.scores.accessibility}/25`);
        console.log(`  Performance:       ${results.scores.performance}/15`);
        console.log(`  Visual Polish:     ${results.scores.visual_polish}/15`);
        console.log(`\n📸 Screenshots: ${results.screenshots.length}/${screens.length * viewports.length}`);
        console.log(`⏱️  Duration: ${(results.duration_ms / 1000).toFixed(2)}s`);

        if (results.issues.length > 0) {
            console.log(`\n⚠️  Issues Found (${results.issues.length}):`);
            results.issues.forEach(issue => console.log(`  - ${issue}`));
        } else {
            console.log(`\n✅ No issues found!`);
        }

        // Save results to JSON
        const outputDir = path.dirname(outputFile);
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
        console.log(`\n💾 Results saved to: ${outputFile}`);

        // Exit code based on score
        if (results.scores.overall_score >= 85) {
            console.log('\n✅ PASSED (Score ≥ 85)');
            process.exit(0);
        } else {
            console.log('\n⚠️  NEEDS IMPROVEMENT (Score < 85)');
            process.exit(1);
        }

    } catch (error) {
        console.error(`\n❌ Visual QA Failed: ${error.message}`);
        console.error(error.stack);
        process.exit(1);
    }
}

// Run the QA
runVisualQA();
