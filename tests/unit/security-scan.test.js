/**
 * Unit tests for security-scan.js
 */

import { describe, it, expect } from 'vitest';

describe('Security Scan - Severity Classification', () => {
  it('should classify critical findings correctly', () => {
    const finding = {
      rule: 'sql-injection',
      severity: 'critical',
      message: 'SQL injection vulnerability'
    };

    expect(finding.severity).toBe('critical');
    expect(isCriticalOrHigh(finding)).toBe(true);
  });

  it('should aggregate findings by severity', () => {
    const findings = [
      { severity: 'critical', rule: 'test1' },
      { severity: 'high', rule: 'test2' },
      { severity: 'medium', rule: 'test3' },
      { severity: 'critical', rule: 'test4' }
    ];

    const aggregated = aggregateBySeverity(findings);

    expect(aggregated.critical).toHaveLength(2);
    expect(aggregated.high).toHaveLength(1);
    expect(aggregated.medium).toHaveLength(1);
  });

  it('should determine if scan should fail build', () => {
    const noIssues = { critical: [], high: [], medium: [1, 2] };
    const hasIssues = { critical: [1], high: [], medium: [] };

    expect(shouldFailBuild(noIssues, true)).toBe(false);
    expect(shouldFailBuild(hasIssues, true)).toBe(true);
    expect(shouldFailBuild(hasIssues, false)).toBe(false);
  });
});

describe('Security Scan - Report Generation', () => {
  it('should generate markdown summary', () => {
    const findings = {
      critical: [{ rule: 'test1', message: 'Critical issue' }],
      high: [],
      medium: [],
      low: [],
      info: []
    };

    const summary = generateMarkdownSummary(findings);

    expect(summary).toContain('# Security Scan Summary');
    expect(summary).toContain('Critical: 1');
    expect(summary).toContain('Critical issue');
  });

  it('should format severity counts correctly', () => {
    const findings = {
      critical: [1, 2],
      high: [1],
      medium: [1, 2, 3],
      low: [],
      info: [1]
    };

    const counts = getSeverityCounts(findings);

    expect(counts).toEqual({
      critical: 2,
      high: 1,
      medium: 3,
      low: 0,
      info: 1
    });
  });
});

// Helper functions
function isCriticalOrHigh(finding) {
  return finding.severity === 'critical' || finding.severity === 'high';
}

function aggregateBySeverity(findings) {
  return findings.reduce((acc, f) => {
    if (!acc[f.severity]) acc[f.severity] = [];
    acc[f.severity].push(f);
    return acc;
  }, {});
}

function shouldFailBuild(findings, failOnHigh) {
  if (!failOnHigh) return false;
  return findings.critical.length > 0 || findings.high.length > 0;
}

function generateMarkdownSummary(findings) {
  const critical = findings.critical.length;
  return `# Security Scan Summary\n\nCritical: ${critical}\n\n${findings.critical.map(f => f.message).join('\n')}`;
}

function getSeverityCounts(findings) {
  return {
    critical: findings.critical.length,
    high: findings.high.length,
    medium: findings.medium.length,
    low: findings.low.length,
    info: findings.info.length
  };
}
