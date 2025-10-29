#!/usr/bin/env node

/**
 * Security Scanning Module
 *
 * Purpose: Static security analysis using Semgrep (JS/TS) and Bandit (Python)
 * Integrates with Software Factory pipeline to identify security vulnerabilities
 * before code generation and deployment.
 *
 * Usage:
 *   node scripts/security-scan.js \
 *     --session-dir .claude/idea-to-design/session-X \
 *     --source-dirs src/,scripts/,apps/ \
 *     [--semgrep-only] [--bandit-only] [--fail-on-high]
 *
 * Features:
 * - Runs Semgrep for JavaScript/TypeScript security analysis
 * - Runs Bandit for Python security analysis
 * - Generates aggregated security summary
 * - Supports failing builds on high-severity findings
 * - Integrates with backlog sync for remediation tracking
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================================
// CLI ARGUMENT PARSING
// ============================================================================

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index !== -1 && args[index + 1] ? args[index + 1] : null;
};

const sessionDir = getArg('--session-dir') || '.claude/idea-to-design/security-scan';
const sourceDirs = (getArg('--source-dirs') || 'src/,scripts/,apps/').split(',').map(d => d.trim());
const semgrepOnly = args.includes('--semgrep-only');
const banditOnly = args.includes('--bandit-only');
const failOnHigh = args.includes('--fail-on-high');

console.log('🔒 Security Scanning Module');
console.log(`   Session: ${sessionDir}`);
console.log(`   Source Dirs: ${sourceDirs.join(', ')}`);
console.log(`   Mode: ${semgrepOnly ? 'Semgrep Only' : banditOnly ? 'Bandit Only' : 'Full Scan'}`);
console.log(`   Fail on High: ${failOnHigh ? 'Yes' : 'No'}\n`);

// ============================================================================
// TOOL AVAILABILITY CHECKS
// ============================================================================

/**
 * Check if Semgrep is installed
 */
function isSemgrepAvailable() {
  try {
    execSync('semgrep --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Check if Bandit is installed
 */
function isBanditAvailable() {
  try {
    execSync('bandit --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Get tool versions
 */
function getToolVersions() {
  const versions = {};

  if (isSemgrepAvailable()) {
    try {
      const version = execSync('semgrep --version', { encoding: 'utf8' }).trim();
      versions.semgrep = version;
    } catch (error) {
      versions.semgrep = 'unknown';
    }
  }

  if (isBanditAvailable()) {
    try {
      const version = execSync('bandit --version', { encoding: 'utf8' }).trim();
      versions.bandit = version;
    } catch (error) {
      versions.bandit = 'unknown';
    }
  }

  return versions;
}

// ============================================================================
// SEMGREP SCANNING
// ============================================================================

/**
 * Run Semgrep security scan
 */
function runSemgrep(sourceDirs, outputDir) {
  console.log('🔍 Running Semgrep scan...\n');

  if (!isSemgrepAvailable()) {
    console.warn('⚠️  Semgrep not installed. Skipping.');
    console.warn('   Install: pip install semgrep OR brew install semgrep\n');
    return null;
  }

  // Filter for existing directories
  const existingDirs = sourceDirs.filter(dir => fs.existsSync(dir));

  if (existingDirs.length === 0) {
    console.warn('⚠️  No source directories found for Semgrep scan\n');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const reportPath = path.join(outputDir, `semgrep-report-${timestamp}.json`);

  try {
    // Run Semgrep with auto config (uses registry rules)
    const command = `semgrep --config=auto --json --output=${reportPath} ${existingDirs.join(' ')}`;

    console.log(`   Command: ${command}`);
    execSync(command, {
      stdio: ['ignore', 'pipe', 'pipe'],
      encoding: 'utf8'
    });

    console.log(`✅ Semgrep scan complete: ${reportPath}\n`);

    // Read and parse results
    const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
    return { report, reportPath };
  } catch (error) {
    // Semgrep exits with code 1 if findings exist, which is expected
    if (fs.existsSync(reportPath)) {
      console.log(`✅ Semgrep scan complete (with findings): ${reportPath}\n`);
      const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
      return { report, reportPath };
    }

    console.error('❌ Semgrep scan failed');
    console.error(`   Error: ${error.message}\n`);
    return null;
  }
}

/**
 * Parse Semgrep results
 */
function parseSemgrepResults(report) {
  const findings = {
    critical: [],
    high: [],
    medium: [],
    low: [],
    info: []
  };

  if (!report || !report.results) {
    return findings;
  }

  report.results.forEach(result => {
    const severity = result.extra?.severity?.toLowerCase() || 'info';
    const finding = {
      rule: result.check_id,
      message: result.extra?.message || result.extra?.lines || 'No message',
      file: result.path,
      line: result.start?.line || 0,
      severity: severity,
      category: result.extra?.metadata?.category || 'security',
      cwe: result.extra?.metadata?.cwe || [],
      owasp: result.extra?.metadata?.owasp || []
    };

    if (findings[severity]) {
      findings[severity].push(finding);
    } else {
      findings.info.push(finding);
    }
  });

  return findings;
}

// ============================================================================
// BANDIT SCANNING
// ============================================================================

/**
 * Run Bandit security scan
 */
function runBandit(sourceDirs, outputDir) {
  console.log('🐍 Running Bandit scan...\n');

  if (!isBanditAvailable()) {
    console.warn('⚠️  Bandit not installed. Skipping.');
    console.warn('   Install: pip install bandit\n');
    return null;
  }

  // Filter for existing Python directories
  const existingDirs = sourceDirs.filter(dir => {
    if (!fs.existsSync(dir)) return false;
    // Check if directory contains Python files
    try {
      const hasPython = execSync(`find ${dir} -name "*.py" | head -n 1`, { encoding: 'utf8' }).trim();
      return hasPython.length > 0;
    } catch (error) {
      return false;
    }
  });

  if (existingDirs.length === 0) {
    console.warn('⚠️  No Python files found for Bandit scan\n');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const reportPath = path.join(outputDir, `bandit-report-${timestamp}.json`);

  try {
    // Run Bandit with JSON output
    const command = `bandit -r ${existingDirs.join(' ')} -f json -o ${reportPath}`;

    console.log(`   Command: ${command}`);
    execSync(command, {
      stdio: ['ignore', 'pipe', 'pipe'],
      encoding: 'utf8'
    });

    console.log(`✅ Bandit scan complete: ${reportPath}\n`);

    // Read and parse results
    const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
    return { report, reportPath };
  } catch (error) {
    // Bandit may exit with non-zero if findings exist
    if (fs.existsSync(reportPath)) {
      console.log(`✅ Bandit scan complete (with findings): ${reportPath}\n`);
      const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
      return { report, reportPath };
    }

    console.error('❌ Bandit scan failed');
    console.error(`   Error: ${error.message}\n`);
    return null;
  }
}

/**
 * Parse Bandit results
 */
function parseBanditResults(report) {
  const findings = {
    critical: [],
    high: [],
    medium: [],
    low: [],
    info: []
  };

  if (!report || !report.results) {
    return findings;
  }

  report.results.forEach(result => {
    const severity = result.issue_severity?.toLowerCase() || 'info';
    const finding = {
      rule: result.test_id,
      message: result.issue_text || 'No message',
      file: result.filename,
      line: result.line_number || 0,
      severity: severity,
      category: 'security',
      confidence: result.issue_confidence?.toLowerCase() || 'unknown',
      cwe: result.issue_cwe ? [result.issue_cwe] : []
    };

    if (findings[severity]) {
      findings[severity].push(finding);
    } else {
      findings.info.push(finding);
    }
  });

  return findings;
}

// ============================================================================
// SUMMARY GENERATION
// ============================================================================

/**
 * Aggregate findings from all tools
 */
function aggregateFindings(semgrepFindings, banditFindings) {
  const aggregated = {
    critical: [],
    high: [],
    medium: [],
    low: [],
    info: []
  };

  // Merge findings from both tools
  ['critical', 'high', 'medium', 'low', 'info'].forEach(severity => {
    if (semgrepFindings && semgrepFindings[severity]) {
      aggregated[severity].push(...semgrepFindings[severity].map(f => ({ ...f, tool: 'semgrep' })));
    }
    if (banditFindings && banditFindings[severity]) {
      aggregated[severity].push(...banditFindings[severity].map(f => ({ ...f, tool: 'bandit' })));
    }
  });

  return aggregated;
}

/**
 * Generate markdown security summary
 */
function generateSecuritySummary(findings, toolVersions, semgrepReport, banditReport) {
  const timestamp = new Date().toISOString();
  const totalFindings = Object.values(findings).reduce((sum, arr) => sum + arr.length, 0);

  let summary = `# Security Scan Summary

**Generated**: ${timestamp}
**Total Findings**: ${totalFindings}

---

## Overview

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 Critical | ${findings.critical.length} | ${findings.critical.length > 0 ? '⚠️ Action Required' : '✅ None'} |
| 🟠 High | ${findings.high.length} | ${findings.high.length > 0 ? '⚠️ Action Required' : '✅ None'} |
| 🟡 Medium | ${findings.medium.length} | ${findings.medium.length > 0 ? '⚠️ Review Recommended' : '✅ None'} |
| 🔵 Low | ${findings.low.length} | ${findings.low.length > 0 ? 'ℹ️ Review Optional' : '✅ None'} |
| ⚪ Info | ${findings.info.length} | ${findings.info.length > 0 ? 'ℹ️ Informational' : '✅ None'} |

---

## Tools Used

`;

  if (toolVersions.semgrep) {
    summary += `- **Semgrep**: ${toolVersions.semgrep}\n`;
  }
  if (toolVersions.bandit) {
    summary += `- **Bandit**: ${toolVersions.bandit}\n`;
  }

  summary += '\n---\n\n';

  // Critical findings
  if (findings.critical.length > 0) {
    summary += `## 🔴 Critical Findings (${findings.critical.length})\n\n`;
    summary += '**Action**: These must be fixed before deployment.\n\n';
    findings.critical.forEach((finding, idx) => {
      summary += `### ${idx + 1}. ${finding.rule}\n`;
      summary += `- **File**: \`${finding.file}:${finding.line}\`\n`;
      summary += `- **Tool**: ${finding.tool}\n`;
      summary += `- **Message**: ${finding.message}\n`;
      if (finding.cwe && finding.cwe.length > 0) {
        summary += `- **CWE**: ${finding.cwe.join(', ')}\n`;
      }
      summary += '\n';
    });
  }

  // High findings
  if (findings.high.length > 0) {
    summary += `## 🟠 High Severity Findings (${findings.high.length})\n\n`;
    summary += '**Action**: Should be fixed before production release.\n\n';
    findings.high.forEach((finding, idx) => {
      summary += `### ${idx + 1}. ${finding.rule}\n`;
      summary += `- **File**: \`${finding.file}:${finding.line}\`\n`;
      summary += `- **Tool**: ${finding.tool}\n`;
      summary += `- **Message**: ${finding.message}\n`;
      if (finding.cwe && finding.cwe.length > 0) {
        summary += `- **CWE**: ${finding.cwe.join(', ')}\n`;
      }
      summary += '\n';
    });
  }

  // Medium findings
  if (findings.medium.length > 0) {
    summary += `## 🟡 Medium Severity Findings (${findings.medium.length})\n\n`;
    summary += '**Action**: Review and address during development.\n\n';
    summary += '<details>\n<summary>Click to expand</summary>\n\n';
    findings.medium.forEach((finding, idx) => {
      summary += `### ${idx + 1}. ${finding.rule}\n`;
      summary += `- **File**: \`${finding.file}:${finding.line}\`\n`;
      summary += `- **Tool**: ${finding.tool}\n`;
      summary += `- **Message**: ${finding.message}\n\n`;
    });
    summary += '</details>\n\n';
  }

  // Low findings
  if (findings.low.length > 0) {
    summary += `## 🔵 Low Severity Findings (${findings.low.length})\n\n`;
    summary += '**Action**: Optional improvements for security hardening.\n\n';
    summary += '<details>\n<summary>Click to expand</summary>\n\n';
    findings.low.forEach((finding, idx) => {
      summary += `${idx + 1}. **${finding.rule}** - \`${finding.file}:${finding.line}\`\n`;
    });
    summary += '\n</details>\n\n';
  }

  // Remediation recommendations
  summary += `---

## Remediation Guidance

### Immediate Actions (Critical & High)
${findings.critical.length + findings.high.length === 0 ? '✅ No immediate actions required.\n' : `
1. Review all critical and high severity findings
2. Create remediation plan with timeline
3. Assign fixes to development team
4. Re-scan after fixes applied
5. Track progress in issue tracker
`}

### Best Practices
- Run security scans on every commit (CI/CD integration)
- Address findings before code review
- Use security linters in IDE/editor
- Keep dependencies updated (use \`npm audit\` or \`pip-audit\`)
- Follow OWASP secure coding guidelines

### Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Semgrep Rules](https://semgrep.dev/explore)
- [Bandit Docs](https://bandit.readthedocs.io/)

---

## Report Files

`;

  if (semgrepReport) {
    summary += `- **Semgrep**: \`${semgrepReport}\`\n`;
  }
  if (banditReport) {
    summary += `- **Bandit**: \`${banditReport}\`\n`;
  }

  summary += `\n---

**Next Steps**:
1. Review findings in detail
2. Prioritize remediation based on severity
3. Create backlog items for tracking
4. Re-run scan after fixes
`;

  return summary;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  // Ensure output directory exists
  const securityDir = path.join(sessionDir, 'security');
  if (!fs.existsSync(securityDir)) {
    fs.mkdirSync(securityDir, { recursive: true });
  }

  // Get tool versions
  const toolVersions = getToolVersions();
  console.log('📊 Tool Versions:');
  if (toolVersions.semgrep) console.log(`   Semgrep: ${toolVersions.semgrep}`);
  if (toolVersions.bandit) console.log(`   Bandit: ${toolVersions.bandit}`);
  console.log('');

  // Run scans
  let semgrepResult = null;
  let banditResult = null;

  if (!banditOnly) {
    semgrepResult = runSemgrep(sourceDirs, securityDir);
  }

  if (!semgrepOnly) {
    banditResult = runBandit(sourceDirs, securityDir);
  }

  // Parse results
  const semgrepFindings = semgrepResult ? parseSemgrepResults(semgrepResult.report) : null;
  const banditFindings = banditResult ? parseBanditResults(banditResult.report) : null;

  // Aggregate findings
  const findings = aggregateFindings(semgrepFindings, banditFindings);

  // Generate summary
  console.log('📝 Generating security summary...\n');
  const summary = generateSecuritySummary(
    findings,
    toolVersions,
    semgrepResult?.reportPath,
    banditResult?.reportPath
  );

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const summaryPath = path.join(securityDir, `security-summary-${timestamp}.md`);
  fs.writeFileSync(summaryPath, summary);

  console.log(`✅ Security summary: ${summaryPath}\n`);

  // Print summary
  console.log('='.repeat(60));
  console.log('📊 Security Scan Results');
  console.log('='.repeat(60));
  console.log(`Critical:  ${findings.critical.length} 🔴`);
  console.log(`High:      ${findings.high.length} 🟠`);
  console.log(`Medium:    ${findings.medium.length} 🟡`);
  console.log(`Low:       ${findings.low.length} 🔵`);
  console.log(`Info:      ${findings.info.length} ⚪`);
  console.log('='.repeat(60));

  // Fail build if requested and high/critical findings exist
  if (failOnHigh && (findings.critical.length > 0 || findings.high.length > 0)) {
    console.error('\n❌ Build failed: High or critical security findings detected');
    console.error(`   Critical: ${findings.critical.length}, High: ${findings.high.length}`);
    console.error(`   Review: ${summaryPath}`);
    process.exit(1);
  }

  if (findings.critical.length + findings.high.length > 0) {
    console.warn('\n⚠️  Security findings require attention');
    console.warn(`   Review: ${summaryPath}`);
  } else {
    console.log('\n✅ No critical or high severity findings');
  }
}

// Run main function
main().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
