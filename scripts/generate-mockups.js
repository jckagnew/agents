#!/usr/bin/env node
/**
 * Template-Based Mockup Generator
 * Reads requirements JSON and generates HTML mockups for 3 variations
 *
 * Usage:
 *   node scripts/generate-mockups.js \
 *     --requirements .claude/idea-to-design/session-X/requirements/iteration-0.json \
 *     --output-dir .claude/idea-to-design/session-X/mockups/iteration-0
 */

const fs = require('fs');
const path = require('path');

// Parse command-line arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const requirementsFile = getArg('--requirements');
const outputDir = getArg('--output-dir');

if (!requirementsFile || !outputDir) {
    console.error('Usage: node generate-mockups.js --requirements <path> --output-dir <path>');
    process.exit(1);
}

// Read requirements
const requirements = JSON.parse(fs.readFileSync(requirementsFile, 'utf8'));

console.log('📋 Generating mockups from requirements...');
console.log(`   App: ${requirements.app_name}`);
console.log(`   Type: ${requirements.app_type}`);
console.log(`   Style: ${requirements.design_preferences?.style || 'modern'}`);
console.log(`   Color: ${requirements.design_preferences?.primary_color || '#4285F4'}`);

// Template generator functions
function generateSplash(requirements, variation) {
    const appName = requirements.app_name || 'My App';
    const description = requirements.description || 'Welcome to our app';
    const primaryColor = requirements.design_preferences?.primary_color || '#4285F4';
    const style = requirements.design_preferences?.style || 'modern';

    // Variation-specific adjustments
    let gradient, buttonStyle, layout;

    if (variation === 'a') {
        // Option A: Safe & Familiar (generous whitespace, calm)
        gradient = `linear-gradient(135deg, ${primaryColor} 0%, ${adjustColor(primaryColor, 20)} 100%)`;
        buttonStyle = 'border-radius: 28px; padding: 16px 48px;';
        layout = 'max-width: 600px; padding: 48px 24px;';
    } else if (variation === 'b') {
        // Option B: Bold & Innovative (vibrant, energetic)
        gradient = `linear-gradient(135deg, ${primaryColor} 0%, ${adjustColor(primaryColor, -30)} 50%, ${adjustColor(primaryColor, 40)} 100%)`;
        buttonStyle = 'border-radius: 12px; padding: 18px 56px; transform: skewX(-5deg);';
        layout = 'max-width: 800px; padding: 64px 32px;';
    } else {
        // Option C: Balanced (middle ground)
        gradient = `linear-gradient(135deg, ${primaryColor} 0%, ${adjustColor(primaryColor, 15)} 100%)`;
        buttonStyle = 'border-radius: 24px; padding: 16px 40px;';
        layout = 'max-width: 700px; padding: 56px 28px;';
    }

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${appName} - Welcome</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: ${gradient};
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .container {
            text-align: center;
            ${layout}
        }

        h1 {
            font-size: ${variation === 'b' ? '56px' : '48px'};
            font-weight: 700;
            margin-bottom: 16px;
            line-height: 1.2;
        }

        p {
            font-size: ${variation === 'b' ? '22px' : '20px'};
            margin-bottom: 32px;
            opacity: 0.95;
            line-height: 1.6;
        }

        button {
            background: white;
            color: ${primaryColor};
            border: none;
            font-size: 18px;
            font-weight: 600;
            ${buttonStyle}
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px) ${variation === 'b' ? 'skewX(-5deg)' : ''};
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        .icon {
            font-size: ${variation === 'b' ? '96px' : '80px'};
            margin-bottom: 24px;
        }

        @media (max-width: 768px) {
            h1 { font-size: 36px; }
            p { font-size: 18px; }
            .icon { font-size: 64px; }
        }

        @media (max-width: 375px) {
            h1 { font-size: 28px; }
            p { font-size: 16px; }
            button { padding: 14px 36px; font-size: 16px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">${getIcon(requirements.app_type)}</div>
        <h1>${appName}</h1>
        <p>${description}</p>
        <button>Get Started</button>
    </div>
</body>
</html>`;
}

function generateDashboard(requirements, variation) {
    const appName = requirements.app_name || 'My App';
    const primaryColor = requirements.design_preferences?.primary_color || '#4285F4';
    const features = requirements.features?.must_have || ['Feature 1', 'Feature 2', 'Feature 3'];

    // Variation-specific card layouts
    let gridCols, cardStyle, headingSize;

    if (variation === 'a') {
        // Option A: Spacious, fewer cards
        gridCols = 'repeat(auto-fit, minmax(280px, 1fr))';
        cardStyle = 'padding: 32px; border-radius: 16px;';
        headingSize = '32px';
    } else if (variation === 'b') {
        // Option B: Dense, more cards
        gridCols = 'repeat(auto-fit, minmax(220px, 1fr))';
        cardStyle = 'padding: 20px; border-radius: 8px; border-left: 4px solid ' + primaryColor + ';';
        headingSize = '28px';
    } else {
        // Option C: Balanced
        gridCols = 'repeat(auto-fit, minmax(250px, 1fr))';
        cardStyle = 'padding: 24px; border-radius: 12px;';
        headingSize = '30px';
    }

    // Generate metric cards (max 3 for option A, 4 for others)
    const maxCards = variation === 'a' ? 3 : 4;
    const metrics = [
        { label: 'Total', value: '127', unit: '' },
        { label: 'Active', value: '89', unit: '' },
        { label: 'Progress', value: '70', unit: '%' },
        { label: 'Score', value: '8.5', unit: '/10' }
    ].slice(0, maxCards);

    const metricCards = metrics.map(m => `
        <div class="card">
            <h3>${m.label}</h3>
            <div>
                <span class="value">${m.value}</span>
                <span class="unit">${m.unit}</span>
            </div>
        </div>
    `).join('');

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - ${appName}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #F5F5F5;
            padding: 24px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        h1 {
            font-size: ${headingSize};
            color: ${primaryColor};
            margin-bottom: 24px;
        }

        .metrics {
            display: grid;
            grid-template-columns: ${gridCols};
            gap: 24px;
            margin-bottom: 32px;
        }

        .card {
            background: white;
            ${cardStyle}
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.2s, transform 0.2s;
        }

        .card:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }

        .card h3 {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .card .value {
            font-size: 36px;
            color: ${primaryColor};
            font-weight: 700;
        }

        .card .unit {
            font-size: 16px;
            color: #999;
        }

        .actions {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }

        button {
            background: ${primaryColor};
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border-radius: ${variation === 'b' ? '8px' : '24px'};
            cursor: pointer;
            transition: background 0.2s;
        }

        button:hover {
            background: ${adjustColor(primaryColor, -15)};
        }

        @media (max-width: 768px) {
            h1 { font-size: 24px; }
            .metrics { grid-template-columns: 1fr; }
            .actions { flex-direction: column; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard</h1>
        <div class="metrics">
            ${metricCards}
        </div>
        <div class="actions">
            <button>Primary Action</button>
            <button style="background: #34A853;">Secondary Action</button>
        </div>
    </div>
</body>
</html>`;
}

function generateSettings(requirements, variation) {
    const appName = requirements.app_name || 'My App';
    const primaryColor = requirements.design_preferences?.primary_color || '#4285F4';

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings - ${appName}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #F5F5F5;
            padding: 24px;
            color: #333;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        h1 {
            font-size: 32px;
            color: ${primaryColor};
            margin-bottom: 24px;
        }

        .section {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .section h2 {
            font-size: 18px;
            margin-bottom: 16px;
            color: #333;
        }

        .setting {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #E0E0E0;
        }

        .setting:last-child {
            border-bottom: none;
        }

        .setting label {
            font-size: 16px;
            color: #666;
        }

        button {
            background: ${primaryColor};
            color: white;
            border: none;
            padding: 12px 32px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 24px;
            cursor: pointer;
            margin-top: 16px;
        }

        @media (max-width: 768px) {
            h1 { font-size: 24px; }
            .section { padding: 16px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Settings</h1>
        <div class="section">
            <h2>General</h2>
            <div class="setting">
                <label>Notifications</label>
                <input type="checkbox" checked>
            </div>
            <div class="setting">
                <label>Dark Mode</label>
                <input type="checkbox">
            </div>
        </div>
        <button>Save Changes</button>
    </div>
</body>
</html>`;
}

// Helper functions
function adjustColor(hex, percent) {
    // Simple color adjustment (lighten/darken)
    const num = parseInt(hex.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return '#' + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
        (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
        (B < 255 ? B < 1 ? 0 : B : 255))
        .toString(16).slice(1).toUpperCase();
}

function getIcon(appType) {
    const icons = {
        health_tracking: '💪',
        e_commerce: '🛒',
        dashboard: '📊',
        social: '💬',
        productivity: '✅',
        default: '🚀'
    };
    return icons[appType] || icons.default;
}

// Generate mockups for all 3 variations
const variations = ['a', 'b', 'c'];
const variationNames = {
    a: 'Safe & Familiar',
    b: 'Bold & Innovative',
    c: 'Balanced'
};

console.log('\n🎨 Generating 3 mockup variations...\n');

for (const variation of variations) {
    const varDir = path.join(outputDir, `option-${variation}`);

    // Create directory
    if (!fs.existsSync(varDir)) {
        fs.mkdirSync(varDir, { recursive: true });
    }

    console.log(`📁 Option ${variation.toUpperCase()}: ${variationNames[variation]}`);

    // Generate HTML files
    const files = {
        'splash.html': generateSplash(requirements, variation),
        'dashboard.html': generateDashboard(requirements, variation),
        'settings.html': generateSettings(requirements, variation)
    };

    for (const [filename, content] of Object.entries(files)) {
        const filepath = path.join(varDir, filename);
        fs.writeFileSync(filepath, content);
        console.log(`   ✅ ${filename}`);
    }

    // Create README with design rationale
    const readme = `# Option ${variation.toUpperCase()}: ${variationNames[variation]}

## Design Strategy
${variation === 'a' ? 'Conservative approach using proven patterns with generous whitespace.' :
      variation === 'b' ? 'Bold and innovative with vibrant colors and unique layouts.' :
                          'Balanced approach blending familiarity with modern flair.'}

## Brand Application
- **Primary Color**: ${requirements.design_preferences?.primary_color || '#4285F4'}
- **Style**: ${requirements.design_preferences?.style || 'modern'}
- **App Type**: ${requirements.app_type}

## Screens Included
- splash.html - Onboarding/welcome screen
- dashboard.html - Main app interface
- settings.html - Configuration screen

## Next Steps
Run Visual QA: \`node scripts/visual-qa-runner.js --mockup-dir ${varDir} --output-file scores/option-${variation}.json\`
`;

    fs.writeFileSync(path.join(varDir, 'README.md'), readme);
    console.log(`   📝 README.md\n`);
}

console.log('✅ Mockup generation complete!');
console.log(`\n📂 Output: ${outputDir}/option-{a,b,c}/`);
console.log('\n🔍 Next: Run Visual QA to score the mockups');
console.log(`   node scripts/visual-qa-runner.js --mockup-dir ${outputDir}/option-a --output-file ${path.dirname(outputDir)}/scores/iteration-0-option-a.json`);

process.exit(0);
