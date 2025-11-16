#!/usr/bin/env node

/**
 * Design Version Validation Script
 *
 * Verifies that the Weight Tracker design artifacts are present, valid, and match
 * the expected hashes before allowing QA or deployment to proceed.
 *
 * Exit codes:
 *   0 - All checks passed
 *   1 - Validation failed (missing files, hash mismatch, or placeholder values)
 *
 * Usage:
 *   node scripts/check-design-version.js
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  bold: '\x1b[1m',
};

const ROOT = path.resolve(__dirname, '..');
const MANIFEST_PATH = path.join(ROOT, 'software-factory/generated-apps/weight-tracker-nextjs/design_version.json');

let exitCode = 0;
const errors = [];
const warnings = [];
const info = [];

/**
 * Print formatted message
 */
function print(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

/**
 * Print section header
 */
function printHeader(title) {
  print(`\n${colors.bold}━━━ ${title} ━━━${colors.reset}`, colors.blue);
}

/**
 * Record error and set exit code
 */
function error(message) {
  errors.push(message);
  exitCode = 1;
}

/**
 * Record warning
 */
function warn(message) {
  warnings.push(message);
}

/**
 * Record info message
 */
function addInfo(message) {
  info.push(message);
}

/**
 * Compute SHA256 hash of a file
 */
function computeSHA256(filePath) {
  try {
    const content = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(content).digest('hex');
  } catch (err) {
    throw new Error(`Failed to compute SHA256: ${err.message}`);
  }
}

/**
 * Compute concatenated MD5 hash of all PNG files in a directory
 */
function computeBaselineHash(dirPath) {
  try {
    if (!fs.existsSync(dirPath)) {
      throw new Error(`Directory does not exist: ${dirPath}`);
    }

    const files = fs.readdirSync(dirPath)
      .filter(f => f.endsWith('.png'))
      .sort(); // Sort for consistent ordering

    if (files.length === 0) {
      throw new Error(`No PNG files found in ${dirPath}`);
    }

    // Concatenate MD5 hashes of all files
    let concatenated = '';
    for (const file of files) {
      const filePath = path.join(dirPath, file);
      const content = fs.readFileSync(filePath);
      const md5 = crypto.createHash('md5').update(content).digest('hex');
      concatenated += md5;
    }

    // Return SHA256 of the concatenated MD5 hashes
    return crypto.createHash('sha256').update(concatenated).digest('hex');
  } catch (err) {
    throw new Error(`Failed to compute baseline hash: ${err.message}`);
  }
}

/**
 * Check if a value is a placeholder
 */
function isPlaceholder(value) {
  return !value || value === '<TBD>' || value.includes('TBD') || value.includes('TODO');
}

/**
 * Main validation logic
 */
function validateDesignVersion() {
  printHeader('Design Version Validation');
  print(`Validating Weight Tracker design artifacts...\n`);

  // Step 1: Check manifest exists
  printHeader('1. Checking Design Version Manifest');
  if (!fs.existsSync(MANIFEST_PATH)) {
    error(`❌ Design version manifest not found: ${MANIFEST_PATH}`);
    print(`   ${colors.red}Create the manifest file to track design version.${colors.reset}`);
    return;
  }
  print(`✅ Manifest found: ${MANIFEST_PATH}`);

  // Step 2: Parse manifest
  printHeader('2. Parsing Manifest');
  let manifest;
  try {
    const content = fs.readFileSync(MANIFEST_PATH, 'utf8');
    manifest = JSON.parse(content);
    print(`✅ Manifest parsed successfully`);
    addInfo(`Design Version: ${manifest.design_version || 'unknown'}`);
    addInfo(`Status: ${manifest.status || 'unknown'}`);
    addInfo(`Last Updated: ${manifest.last_updated || 'unknown'}`);
  } catch (err) {
    error(`❌ Failed to parse manifest: ${err.message}`);
    return;
  }

  // Step 3: Check required fields
  printHeader('3. Validating Required Fields');
  const requiredFields = ['design_version', 'figma_file', 'spec_path', 'spec_hash', 'baseline_path', 'baseline_hash'];
  let hasPlaceholders = false;

  for (const field of requiredFields) {
    if (!manifest[field]) {
      error(`❌ Missing required field: ${field}`);
    } else if (isPlaceholder(manifest[field])) {
      warn(`⚠️  Field '${field}' has placeholder value: ${manifest[field]}`);
      hasPlaceholders = true;
    } else {
      print(`✅ ${field}: ${manifest[field]}`);
    }
  }

  if (hasPlaceholders) {
    error(`❌ Manifest contains placeholder values (<TBD>). Update with actual hashes.`);
    print(`\n   ${colors.yellow}To compute spec hash:${colors.reset}`);
    print(`   ${colors.yellow}  node -e "const crypto=require('crypto');const fs=require('fs');console.log(crypto.createHash('sha256').update(fs.readFileSync('${manifest.spec_path}')).digest('hex'))"${colors.reset}`);
    print(`\n   ${colors.yellow}To compute baseline hash (after capturing screenshots):${colors.reset}`);
    print(`   ${colors.yellow}  node scripts/check-design-version.js --compute-baseline${colors.reset}`);
  }

  // Step 4: Verify spec file exists
  printHeader('4. Checking Design Spec File');
  const specPath = path.join(ROOT, manifest.spec_path);
  if (!fs.existsSync(specPath)) {
    error(`❌ Design spec file not found: ${specPath}`);
  } else {
    print(`✅ Spec file exists: ${specPath}`);

    // Verify spec hash (if not placeholder)
    if (!isPlaceholder(manifest.spec_hash)) {
      try {
        const actualHash = computeSHA256(specPath);
        if (actualHash === manifest.spec_hash) {
          print(`✅ Spec hash matches: ${actualHash.substring(0, 16)}...`);
        } else {
          error(`❌ Spec hash mismatch!`);
          print(`   Expected: ${manifest.spec_hash}`);
          print(`   Actual:   ${actualHash}`);
          print(`   ${colors.red}Design spec has changed since manifest was updated.${colors.reset}`);
        }
      } catch (err) {
        error(`❌ Failed to verify spec hash: ${err.message}`);
      }
    } else {
      warn(`⚠️  Skipping spec hash verification (placeholder value)`);
    }
  }

  // Step 5: Verify baseline directory exists
  printHeader('5. Checking Baseline Screenshot Directory');
  const baselinePath = path.join(ROOT, manifest.baseline_path);
  if (!fs.existsSync(baselinePath)) {
    error(`❌ Baseline directory not found: ${baselinePath}`);
    print(`   ${colors.yellow}Create directory and capture golden screenshots after implementing v2 UI.${colors.reset}`);
  } else {
    const pngFiles = fs.readdirSync(baselinePath).filter(f => f.endsWith('.png'));
    if (pngFiles.length === 0) {
      error(`❌ No baseline screenshots found in ${baselinePath}`);
      print(`   ${colors.yellow}Capture baseline screenshots after implementing v2 UI.${colors.reset}`);
    } else {
      print(`✅ Baseline directory exists: ${baselinePath}`);
      print(`   Found ${pngFiles.length} PNG file(s)`);

      // Verify baseline hash (if not placeholder)
      if (!isPlaceholder(manifest.baseline_hash)) {
        try {
          const actualHash = computeBaselineHash(baselinePath);
          if (actualHash === manifest.baseline_hash) {
            print(`✅ Baseline hash matches: ${actualHash.substring(0, 16)}...`);
          } else {
            error(`❌ Baseline hash mismatch!`);
            print(`   Expected: ${manifest.baseline_hash}`);
            print(`   Actual:   ${actualHash}`);
            print(`   ${colors.red}Baseline screenshots have changed since manifest was updated.${colors.reset}`);
          }
        } catch (err) {
          error(`❌ Failed to verify baseline hash: ${err.message}`);
        }
      } else {
        warn(`⚠️  Skipping baseline hash verification (placeholder value)`);
      }
    }
  }

  // Step 6: Check implementation status
  printHeader('6. Checking Implementation Status');
  if (manifest.status === 'pending_implementation') {
    error(`❌ Implementation status: ${manifest.status}`);
    print(`   ${colors.red}v2 UI is not yet implemented. QA should not run until implementation is complete.${colors.reset}`);
  } else if (manifest.status === 'implemented') {
    print(`✅ Implementation status: ${manifest.status}`);
  } else {
    warn(`⚠️  Unknown implementation status: ${manifest.status}`);
  }
}

/**
 * Utility function to compute and print baseline hash
 */
function computeBaselineHashUtil() {
  printHeader('Computing Baseline Hash');

  const manifestPath = MANIFEST_PATH;
  if (!fs.existsSync(manifestPath)) {
    print(`${colors.red}❌ Manifest not found: ${manifestPath}${colors.reset}`);
    process.exit(1);
  }

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const baselinePath = path.join(ROOT, manifest.baseline_path);

  if (!fs.existsSync(baselinePath)) {
    print(`${colors.red}❌ Baseline directory not found: ${baselinePath}${colors.reset}`);
    print(`   Create the directory and capture baseline screenshots first.`);
    process.exit(1);
  }

  try {
    const hash = computeBaselineHash(baselinePath);
    print(`${colors.green}✅ Baseline hash computed successfully:${colors.reset}`);
    print(`\n   ${colors.bold}${hash}${colors.reset}\n`);
    print(`Update design_version.json with:`);
    print(`${colors.yellow}  "baseline_hash": "${hash}"${colors.reset}`);
  } catch (err) {
    print(`${colors.red}❌ ${err.message}${colors.reset}`);
    process.exit(1);
  }
}

/**
 * Print summary
 */
function printSummary() {
  printHeader('Validation Summary');

  if (info.length > 0) {
    print(`\n${colors.blue}ℹ️  Information:${colors.reset}`);
    info.forEach(msg => print(`   ${msg}`));
  }

  if (warnings.length > 0) {
    print(`\n${colors.yellow}⚠️  Warnings (${warnings.length}):${colors.reset}`);
    warnings.forEach(msg => print(`   ${msg}`));
  }

  if (errors.length > 0) {
    print(`\n${colors.red}❌ Errors (${errors.length}):${colors.reset}`);
    errors.forEach(msg => print(`   ${msg}`));
    print(`\n${colors.bold}${colors.red}VALIDATION FAILED${colors.reset}`);
    print(`${colors.red}QA and deployment should be blocked until all checks pass.${colors.reset}\n`);
  } else {
    print(`\n${colors.bold}${colors.green}✅ ALL CHECKS PASSED${colors.reset}`);
    print(`${colors.green}Design artifacts are valid and ready for QA/deployment.${colors.reset}\n`);
  }
}

// Main execution
if (process.argv.includes('--compute-baseline')) {
  computeBaselineHashUtil();
} else {
  validateDesignVersion();
  printSummary();
  process.exit(exitCode);
}
