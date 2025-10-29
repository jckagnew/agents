const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const pixelmatch = require('pixelmatch');
const { PNG } = require('pngjs');

/**
 * Weight Tracker Visual QA Test Suite - Complete 7-Screen Coverage
 * Tests ALL screens: Splash, Login, Dashboard, Log Entry, History, Analytics, Settings
 */

const projectRoot = path.resolve(__dirname, '..', '..');
const workspaceRoot = path.resolve(projectRoot, '..', '..', '..');
const manifestPath = path.resolve(projectRoot, 'design_version.json');
let baselineConfig = null;

function loadBaselineConfig() {
    if (!baselineConfig) {
        if (!fs.existsSync(manifestPath)) {
            throw new Error(`Design manifest not found at ${manifestPath}`);
        }
        const manifestRaw = fs.readFileSync(manifestPath, 'utf-8');
        baselineConfig = JSON.parse(manifestRaw);
        // baseline_path is relative to workspace root, not project root
        baselineConfig.baselineDir = path.resolve(workspaceRoot, baselineConfig.baseline_path || '');
    }
    return baselineConfig;
}

function ensureDiffDirectory() {
    const diffDir = path.join(process.cwd(), 'screenshots', 'diff');
    if (!fs.existsSync(diffDir)) {
        fs.mkdirSync(diffDir, { recursive: true });
    }
    return diffDir;
}

async function disableAnimations(page) {
    await page.addStyleTag({
        content: `
            *, *::before, *::after {
                transition-property: none !important;
                transition-duration: 0s !important;
                transition-delay: 0s !important;
                animation-duration: 0.001ms !important;
            }
        `
    });
}

function compareWithBaseline(actualPath, fileName) {
    const config = loadBaselineConfig();
    const baselinePath = path.join(config.baselineDir, fileName);

    const toleranceOverrides = {
        'splash-desktop-1440x900.png': 0.003,
        'splash-tablet-768x1024.png': 0.004,
        'splash-mobile-375x667.png': 0.004
    };

    if (!fs.existsSync(baselinePath)) {
        return {
            match: false,
            diffPath: null,
            reason: `Baseline missing for ${fileName} (${baselinePath})`
        };
    }

    const actual = PNG.sync.read(fs.readFileSync(actualPath));
    const baseline = PNG.sync.read(fs.readFileSync(baselinePath));

    if (actual.width !== baseline.width || actual.height !== baseline.height) {
        return {
            match: false,
            diffPath: null,
            reason: `Size mismatch for ${fileName} (actual ${actual.width}x${actual.height}, baseline ${baseline.width}x${baseline.height})`
        };
    }

    const diff = new PNG({ width: actual.width, height: actual.height });
    const diffPixels = pixelmatch(actual.data, baseline.data, diff.data, actual.width, actual.height, {
        threshold: 0.1,
        alpha: 0.5
    });

    const totalPixels = actual.width * actual.height;
    const diffRatio = diffPixels / totalPixels;
    const tolerance = toleranceOverrides[fileName] ?? 0.003; // Allow limited drift for gradients/anti-aliasing

    if (diffPixels === 0 || diffRatio <= tolerance) {
        return {
            match: true,
            diffPath: null,
            reason: diffPixels === 0 ? 'Exact match' : `Diff below tolerance (${(diffRatio * 100).toFixed(3)}%)`
        };
    }

    const diffDir = ensureDiffDirectory();
    const diffPath = path.join(diffDir, fileName);
    fs.writeFileSync(diffPath, PNG.sync.write(diff));

    return {
        match: false,
        diffPath,
        reason: `Visual diff exceeded threshold (${diffPixels} px, ${(diffRatio * 100).toFixed(3)}%)`
    };
}

function checkDesignVersion() {
    console.log('🔍 Checking design version...');
    try {
        const scriptPath = path.resolve(__dirname, '../../../../../scripts/check-design-version.js');
        execSync(`node "${scriptPath}"`, {
            stdio: 'inherit',
            cwd: path.resolve(__dirname, '../../../../..')
        });
        console.log('✅ Design version validation passed\n');
    } catch (error) {
        console.error('\n❌ Design version validation FAILED');
        console.error('⛔ QA cannot proceed until design artifacts are valid');
        console.error('\nFix the issues above, then re-run visual tests.\n');
        process.exit(1);
    }
}

async function runWeightTrackerQA() {
    checkDesignVersion();

    console.log('🎨 Starting Weight Tracker Visual QA Review (All 7 Screens)...');
    const startTime = Date.now();

    try {
        const launchOptions = { headless: true };
        const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
        if (fs.existsSync(chromePath)) {
            launchOptions.executablePath = chromePath;
        }

        const browser = await chromium.launch(launchOptions);
        const screenshotsDir = path.resolve(process.cwd(), 'screenshots');
        if (!fs.existsSync(screenshotsDir)) {
            fs.mkdirSync(screenshotsDir, { recursive: true });
        }

        const viewports = [
            { name: 'Desktop', width: 1440, height: 900 },
            { name: 'Tablet', width: 768, height: 1024 },
            { name: 'Mobile', width: 375, height: 667 }
        ];

        const results = {
            screens: [],
            screenshots: [],
            diffs: [],
            scores: {},
            issues: [],
            duration: 0
        };

        console.log('\n📱 PHASE 1: Capturing Unauthenticated Screens...');

        // SPLASH SCREEN
        console.log('\n📱 Testing Splash screen...');
        const splashScreen = { name: 'Splash', key: 'splash', viewports: [] };
        
        for (const viewport of viewports) {
            console.log(`  ${viewport.name} (${viewport.width}x${viewport.height})`);
            const context = await browser.newContext();
            const page = await context.newPage();
            await page.setViewportSize({ width: viewport.width, height: viewport.height });

            try {
                await page.goto('http://localhost:3000', { waitUntil: 'networkidle', timeout: 10000 });
                await disableAnimations(page);
                await page.waitForSelector('h1', { timeout: 5000 });
                await page.waitForTimeout(500);

                const fileName = `splash-${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`;
                const screenshotPath = path.join(screenshotsDir, fileName);
                await page.screenshot({ path: screenshotPath, fullPage: true });
                results.screenshots.push(path.join('screenshots', fileName));

                const metrics = await page.evaluate(() => {
                    const heading = document.querySelector('h1, [role="heading"][aria-level="1"]');
                    return {
                        hasH1: !!heading,
                        hasButtons: document.querySelectorAll('button').length
                    };
                });

                const visualResult = compareWithBaseline(screenshotPath, fileName);
                if (!visualResult.match) {
                    console.error(`    ⚠️  Visual mismatch: ${visualResult.reason}`);
                    results.issues.push(`${splashScreen.name} (${viewport.name}): ${visualResult.reason}`);
                }
                if (visualResult.diffPath) {
                    results.diffs.push(path.relative(process.cwd(), visualResult.diffPath));
                }

                splashScreen.viewports.push({
                    viewport: viewport.name,
                    dimensions: `${viewport.width}x${viewport.height}`,
                    metrics,
                    diff: visualResult.diffPath ? path.relative(process.cwd(), visualResult.diffPath) : null,
                    success: visualResult.match
                });
            } catch (error) {
                console.error(`    ❌ Error: ${error.message}`);
                splashScreen.viewports.push({ viewport: viewport.name, error: error.message, success: false });
            }

            await context.close();
        }
        results.screens.push(splashScreen);

        // LOGIN SCREEN
        console.log('\n📱 Testing Login screen...');
        const loginScreen = { name: 'Login', key: 'login', viewports: [] };
        
        for (const viewport of viewports) {
            console.log(`  ${viewport.name} (${viewport.width}x${viewport.height})`);
            const context = await browser.newContext();
            const page = await context.newPage();
            await page.setViewportSize({ width: viewport.width, height: viewport.height });

            try {
                await page.goto('http://localhost:3000', { waitUntil: 'networkidle', timeout: 10000 });
                await disableAnimations(page);
                await page.waitForSelector('button:has-text("Start Your Journey")', { timeout: 5000 });
                await page.click('button:has-text("Start Your Journey")');
                await page.waitForSelector('input[type="text"]', { timeout: 5000 });
                await page.waitForTimeout(500);

                const fileName = `login-${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`;
                const screenshotPath = path.join(screenshotsDir, fileName);
                await page.screenshot({ path: screenshotPath, fullPage: true });
                results.screenshots.push(path.join('screenshots', fileName));

                const metrics = await page.evaluate(() => {
                    const heading = document.querySelector('h1, [role="heading"][aria-level="1"]');
                    return {
                        hasH1: !!heading,
                        hasInputs: document.querySelectorAll('input').length,
                        hasButtons: document.querySelectorAll('button').length
                    };
                });

                const visualResult = compareWithBaseline(screenshotPath, fileName);
                if (!visualResult.match) {
                    console.error(`    ⚠️  Visual mismatch: ${visualResult.reason}`);
                    results.issues.push(`${loginScreen.name} (${viewport.name}): ${visualResult.reason}`);
                }
                if (visualResult.diffPath) {
                    results.diffs.push(path.relative(process.cwd(), visualResult.diffPath));
                }

                loginScreen.viewports.push({
                    viewport: viewport.name,
                    dimensions: `${viewport.width}x${viewport.height}`,
                    metrics,
                    diff: visualResult.diffPath ? path.relative(process.cwd(), visualResult.diffPath) : null,
                    success: visualResult.match
                });
            } catch (error) {
                console.error(`    ❌ Error: ${error.message}`);
                loginScreen.viewports.push({ viewport: viewport.name, error: error.message, success: false });
            }

            await context.close();
        }
        results.screens.push(loginScreen);

        console.log('\n📱 PHASE 2: Capturing Authenticated Screens...');

        const authContext = await browser.newContext();
        await authContext.addInitScript((storedUser) => {
            window.localStorage.setItem('weight-tracker-user', JSON.stringify({ ...storedUser, loginTime: Date.now() }));
        }, { id: 'qa_user', username: 'demo', emoji: '👤' });

        const authenticatedScreens = [
            { name: 'Dashboard', buttonText: null, key: 'dashboard', heading: 'Weight Tracker Pro' },
            { name: 'Log Entry', buttonText: 'Log', key: 'log', heading: 'Log New Entry' },
            { name: 'History', buttonText: 'History', key: 'history', heading: 'Weight History' },
            { name: 'Analytics', buttonText: 'Analytics', key: 'analytics', heading: 'Analytics' },
            { name: 'Settings', buttonText: 'Settings', key: 'settings', heading: 'Settings' }
        ];

        for (const screen of authenticatedScreens) {
            console.log(`\n📱 Testing ${screen.name} screen...`);
            const screenResults = { name: screen.name, buttonText: screen.buttonText, viewports: [] };

            for (const viewport of viewports) {
                console.log(`  ${viewport.name} (${viewport.width}x${viewport.height})`);
                const page = await authContext.newPage();
                await page.setViewportSize({ width: viewport.width, height: viewport.height });

                try {
                    await page.goto('http://localhost:3000', { waitUntil: 'networkidle', timeout: 10000 });
                    await disableAnimations(page);

                    if (screen.buttonText) {
                        await page.waitForTimeout(300);
                        const navButton = page
                            .locator('nav[aria-label="Main navigation"] button:visible')
                            .filter({ hasText: screen.buttonText })
                            .first();
                        await navButton.waitFor({ state: 'visible', timeout: 5000 });
                        await navButton.click();
                        await page.waitForTimeout(500);
                    }

                    await page.waitForTimeout(500);

                    const fileName = `${screen.key}-${viewport.name.toLowerCase()}-${viewport.width}x${viewport.height}.png`;
                    const screenshotPath = path.join(screenshotsDir, fileName);
                    await page.screenshot({ path: screenshotPath, fullPage: true });
                    results.screenshots.push(path.join('screenshots', fileName));

                    const metrics = await page.evaluate(() => {
                        const heading = document.querySelector('h1, [role="heading"][aria-level="1"]');
                        return {
                            hasH1: !!heading,
                            hasButtons: document.querySelectorAll('button').length,
                            hasCards: document.querySelectorAll('[class*="card"]').length
                        };
                    });

                    const visualResult = compareWithBaseline(screenshotPath, fileName);
                    if (!visualResult.match) {
                        console.error(`    ⚠️  Visual mismatch: ${visualResult.reason}`);
                        results.issues.push(`${screen.name} (${viewport.name}): ${visualResult.reason}`);
                    }
                    if (visualResult.diffPath) {
                        results.diffs.push(path.relative(process.cwd(), visualResult.diffPath));
                    }

                    screenResults.viewports.push({
                        viewport: viewport.name,
                        dimensions: `${viewport.width}x${viewport.height}`,
                        metrics,
                        diff: visualResult.diffPath ? path.relative(process.cwd(), visualResult.diffPath) : null,
                        success: visualResult.match
                    });
                } catch (error) {
                    console.error(`    ❌ Error: ${error.message}`);
                    screenResults.viewports.push({ viewport: viewport.name, error: error.message, success: false });
                }

                await page.close();
            }

            results.screens.push(screenResults);
        }

        await authContext.close();
        await browser.close();

        const scoring = calculateQualityScore(results);
        Object.assign(results, scoring);
        results.duration = (Date.now() - startTime) / 1000;

        generateReport(results);
        return results;

    } catch (error) {
        console.error('❌ Critical Error:', error.message);
        return { success: false, error: error.message, overallScore: 0 };
    }
}

function calculateQualityScore(results) {
    const scores = { brandCompliance: 0, responsiveDesign: 0, accessibility: 0, performance: 0, visualPolish: 0 };
    const issues = [];

    let successfulScreens = results.screens.filter(s => s.viewports.filter(v => v.success).length === 3).length;
    scores.brandCompliance = Math.round((successfulScreens / 7) * 25);
    if (successfulScreens < 7) issues.push(`${7 - successfulScreens} screen(s) failed to load in all viewports`);

    const allViewportsWorking = results.screens.every(s => s.viewports.every(v => v.success));
    scores.responsiveDesign = allViewportsWorking ? 20 : 10;
    if (!allViewportsWorking) issues.push('Not all screens are responsive across all viewports');

    let screensWithH1 = results.screens.filter(s => s.viewports.find(v => v.viewport === 'Desktop')?.metrics?.hasH1).length;
    scores.accessibility = Math.round((screensWithH1 / 7) * 25);
    if (screensWithH1 < 7) issues.push(`${7 - screensWithH1} screen(s) missing H1 heading`);

    const successfulLoads = results.screens.reduce((sum, s) => sum + s.viewports.filter(v => v.success).length, 0);
    scores.performance = Math.round((successfulLoads / 21) * 15);

    let screensWithInteractive = results.screens.filter(s => {
        const desktop = s.viewports.find(v => v.viewport === 'Desktop');
        return desktop?.metrics?.hasButtons > 0 || desktop?.metrics?.hasInputs > 0;
    }).length;
    scores.visualPolish = Math.round((screensWithInteractive / 7) * 15);

    const overallScore = Object.values(scores).reduce((sum, s) => sum + s, 0);
    const grade = overallScore >= 90 ? 'A' : overallScore >= 80 ? 'B' : overallScore >= 70 ? 'C' : overallScore >= 60 ? 'D' : 'F';

    return { scores, issues, overallScore, grade };
}

function generateReport(results) {
    console.log('\n📊 Weight Tracker Visual QA Report');
    console.log('===================================');
    console.log(`Overall Score: ${results.overallScore}/100`);
    console.log(`Grade: ${results.grade}`);
    console.log(`Duration: ${results.duration.toFixed(2)}s`);
    console.log(`Screens Tested: ${results.screens.length}/7`);

    console.log('\n📈 Score Breakdown:');
    Object.entries(results.scores).forEach(([key, val]) => {
        const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, s => s.toUpperCase());
        console.log(`  ${label}: ${val}`);
    });

    if (results.issues.length > 0) {
        console.log('\n🚨 Issues Found:');
        results.issues.forEach(issue => console.log(`  - ${issue}`));
    }

    console.log('\n📱 Screen Results:');
    results.screens.forEach(screen => {
        const successCount = screen.viewports.filter(v => v.success).length;
        const status = successCount === 3 ? '✅' : '⚠️';
        console.log(`  ${status} ${screen.name}: ${successCount}/3 viewports passed`);
    });

    console.log(`\n📸 Screenshots: ${results.screenshots.length}/21`);
    if (results.diffs.length > 0) {
        console.log('\n🖼️ Visual Diffs Detected:');
        results.diffs.forEach(diffPath => {
            console.log(`  - ${path.relative(process.cwd(), diffPath)}`);
        });
    }

    const reportPath = `reports/weight-tracker-qa-${new Date().toISOString().split('T')[0]}.json`;
    fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
    console.log(`💾 Report saved to: ${reportPath}`);

    const passed = results.overallScore >= 85 && results.diffs.length === 0;
    console.log(`\n🎯 Status: ${passed ? '✅ PASS' : '❌ FAIL'} (threshold: 85${results.diffs.length > 0 ? ', visual diffs present' : ''})`);
}

if (!fs.existsSync('screenshots')) fs.mkdirSync('screenshots', { recursive: true });
if (!fs.existsSync('reports')) fs.mkdirSync('reports', { recursive: true });

runWeightTrackerQA().then(result => {
    if (result.success === false) {
        console.log('\n❌ Test suite failed');
        process.exit(1);
    } else if (result.overallScore < 85) {
        console.log('\n⚠️ Quality threshold not met');
        process.exit(1);
    } else if (result.diffs && result.diffs.length > 0) {
        console.log('\n❌ Visual diffs detected - see screenshots/diff for details');
        process.exit(1);
    } else {
        console.log('\n✅ All checks passed!');
        process.exit(0);
    }
}).catch(error => {
    console.error('\n❌ Fatal error:', error);
    process.exit(1);
});
