# 🔒 Security Scanning Guide

## Overview

The Software Factory includes automated security scanning using industry-standard static analysis tools to identify vulnerabilities before code reaches production.

**Status**: ✅ Production Ready
**Last Updated**: October 2024

---

## Tools

### Semgrep
**Purpose**: JavaScript/TypeScript static security analysis
**Version**: 1.140.0+
**Coverage**: JavaScript, TypeScript, React, Node.js

**Capabilities**:
- OWASP Top 10 detection
- Common vulnerability patterns
- Security best practices validation
- CWE coverage
- Custom rule support

### Bandit
**Purpose**: Python static security analysis
**Version**: 1.8.0+
**Coverage**: Python 3.x

**Capabilities**:
- Security issue detection
- Code quality checks
- Common vulnerabilities (injection, XSS, etc.)
- Hardcoded secrets detection

---

## Installation

### Prerequisites

**macOS (Homebrew)**:
```bash
# Install Semgrep
brew install semgrep

# Install Bandit
pip install bandit
```

**Linux (pip)**:
```bash
# Install Semgrep
pip install semgrep

# Install Bandit
pip install bandit
```

**Verify Installation**:
```bash
# Check Semgrep
semgrep --version

# Check Bandit
bandit --version
```

---

## Usage

### Quick Start

```bash
# Run full security scan
npm run security:scan

# Run Semgrep only (JavaScript/TypeScript)
npm run security:scan:semgrep

# Run Bandit only (Python)
npm run security:scan:bandit

# Run with strict mode (fail on high severity)
npm run security:scan:strict
```

### Manual Invocation

```bash
# Basic scan
node scripts/security-scan.js \
  --session-dir .claude/idea-to-design/security-scan \
  --source-dirs src/,scripts/,apps/

# Custom source directories
node scripts/security-scan.js \
  --session-dir .claude/idea-to-design/my-session \
  --source-dirs path/to/code,another/path

# Semgrep only
node scripts/security-scan.js \
  --session-dir .claude/idea-to-design/security-scan \
  --source-dirs src/ \
  --semgrep-only

# Fail build on high severity
node scripts/security-scan.js \
  --session-dir .claude/idea-to-design/security-scan \
  --source-dirs src/,scripts/ \
  --fail-on-high
```

---

## Output Files

All reports are saved to `.claude/idea-to-design/[session-dir]/security/`:

### Semgrep Report
**File**: `semgrep-report-TIMESTAMP.json`
**Format**: JSON
**Contents**:
- Detailed findings with file/line locations
- Rule IDs and metadata
- Severity levels
- CWE/OWASP mappings
- Code snippets

### Bandit Report
**File**: `bandit-report-TIMESTAMP.json`
**Format**: JSON
**Contents**:
- Python security issues
- Confidence levels
- Issue severity
- File locations
- Test IDs

### Security Summary
**File**: `security-summary-TIMESTAMP.md`
**Format**: Markdown
**Contents**:
- Executive summary with severity counts
- Critical/High findings (detailed)
- Medium/Low findings (collapsed)
- Remediation guidance
- Links to detailed reports
- Best practices

**Example Summary**:
```markdown
# Security Scan Summary

**Generated**: 2025-10-24T17:21:00.643Z
**Total Findings**: 5

## Overview

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 Critical | 0 | ✅ None |
| 🟠 High | 1 | ⚠️ Action Required |
| 🟡 Medium | 2 | ⚠️ Review Recommended |
| 🔵 Low | 2 | ℹ️ Review Optional |
```

---

## Severity Levels

### 🔴 Critical
**Action**: **Must fix before deployment**
**Timeline**: Immediate
**Examples**:
- SQL injection vulnerabilities
- Remote code execution
- Authentication bypass
- Hardcoded credentials

### 🟠 High
**Action**: **Should fix before production**
**Timeline**: Within sprint
**Examples**:
- XSS vulnerabilities
- CSRF issues
- Insecure deserialization
- Path traversal

### 🟡 Medium
**Action**: Review and address during development
**Timeline**: Next sprint
**Examples**:
- Weak cryptography
- Information disclosure
- Missing security headers
- Insecure randomness

### 🔵 Low
**Action**: Optional improvements
**Timeline**: Backlog
**Examples**:
- Code quality issues
- Best practice violations
- Minor information leaks
- Deprecated functions

### ⚪ Info
**Action**: Informational only
**Timeline**: None
**Examples**:
- Security notes
- Documentation suggestions
- Style recommendations

---

## CI/CD Integration

### GitHub Actions

The security scan runs automatically in CI/CD pipeline after lint and tests.

**Workflow**: `.github/workflows/ci.yml`

```yaml
- name: Install security scanning tools
  run: |
    pip install semgrep bandit

- name: Run Software Factory security scan
  run: |
    npm run security:scan:strict
  continue-on-error: false
```

**Behavior**:
- Runs on all pushes and PRs
- Uses `--fail-on-high` flag
- Fails build if critical/high findings exist
- Uploads reports as artifacts

### Local Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: security-scan
        name: Security Scan
        entry: npm run security:scan
        language: system
        pass_filenames: false
```

---

## Rulesets

### Semgrep Rules

**Default**: `--config=auto` (uses Semgrep Registry)

**Categories**:
- `security`: Security vulnerabilities
- `owasp-top-ten`: OWASP Top 10 issues
- `cwe-top-25`: CWE Top 25 weaknesses
- `best-practices`: Security best practices

**Custom Rules**:
Create `.semgrep.yml` in project root:

```yaml
rules:
  - id: no-console-log-production
    pattern: console.log(...)
    message: "Remove console.log in production"
    severity: WARNING
    languages: [javascript, typescript]
```

### Bandit Configuration

**Default**: All tests enabled

**Custom Config**:
Create `.bandit` in project root:

```ini
[bandit]
exclude: /test,/tests,/migrations
skips: B101,B601

[bandit.plugins]
B201: flask_debug_true
B202: tarfile_unsafe_members
```

---

## Integration with Backlog Sync

High-severity security findings are automatically captured by the backlog sync module.

### Automatic Backlog Creation

When running:
```bash
node scripts/backlog-sync.js --session-dir .claude/idea-to-design/session-X
```

The backlog sync will extract security findings from the latest scan and create issues:

**Example Backlog Item**:
```json
{
  "title": "[Security] SQL Injection in user query",
  "description": "Critical: SQL injection vulnerability found in scripts/database.js:42",
  "priority": "P1",
  "source": "Security Scan (Semgrep)",
  "labels": ["security", "critical", "sql-injection"],
  "status": "todo"
}
```

---

## Best Practices

### Development Workflow

1. **Before Commit**: Run `npm run security:scan`
2. **Review Findings**: Check generated summary
3. **Fix Critical/High**: Address before pushing
4. **Create Issues**: Add medium/low to backlog
5. **Re-scan**: Verify fixes resolved findings

### Code Review

- Include security summary in PR description
- Reviewers verify findings addressed
- No merge if critical/high findings unresolved
- Document accepted risks

### Continuous Improvement

- Review scan results weekly
- Update rulesets quarterly
- Track remediation metrics
- Share learnings with team

---

## Troubleshooting

### Semgrep Issues

**Error: Semgrep not found**
```bash
# Install Semgrep
brew install semgrep
# OR
pip install semgrep
```

**Error: Timeout**
```bash
# Increase timeout for large codebases
semgrep --timeout 300 --config=auto src/
```

**Error: False positives**
```yaml
# Add to .semgrep.yml
rules:
  - id: problematic-rule
    pattern: ...
    options:
      exclude:
        - path/to/false/positive.js
```

### Bandit Issues

**Error: Bandit not found**
```bash
pip install bandit
```

**Error: No Python files**
- Ensure source directories contain `.py` files
- Check directory paths are correct
- Use `--bandit-only` for debugging

**Error: Too many findings**
```ini
# Create .bandit config to skip tests
[bandit]
skips: B101,B601
```

### General Issues

**No findings but code has issues**
- Verify tools installed correctly
- Check source directories exist
- Review ruleset configuration
- Consider custom rules

**Scan too slow**
- Limit source directories
- Use `--semgrep-only` or `--bandit-only`
- Exclude test/vendor directories
- Increase timeout

---

## Security Resources

### OWASP
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [OWASP Security Knowledge Framework](https://www.securityknowledgeframework.org/)

### CWE
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CWE SANS Top 25](https://www.sans.org/top25-software-errors/)

### Tool Documentation
- [Semgrep Docs](https://semgrep.dev/docs/)
- [Semgrep Registry](https://semgrep.dev/explore)
- [Bandit Docs](https://bandit.readthedocs.io/)

### Secure Coding
- [Secure Coding Guidelines](https://wiki.sei.cmu.edu/confluence/display/seccode)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)

---

## Example Scan Session

```bash
# 1. Run security scan
$ npm run security:scan

🔒 Security Scanning Module
   Session: .claude/idea-to-design/security-scan
   Source Dirs: src/, scripts/, apps/
   Mode: Full Scan

🔍 Running Semgrep scan...
✅ Semgrep scan complete

🐍 Running Bandit scan...
✅ Bandit scan complete

📝 Generating security summary...
✅ Security summary created

============================================================
📊 Security Scan Results
============================================================
Critical:  0 🔴
High:      2 🟠
Medium:    5 🟡
Low:       3 🔵
Info:      12 ⚪
============================================================

⚠️  Security findings require attention
   Review: .claude/idea-to-design/security-scan/security/security-summary-2025-10-24.md

# 2. Review findings
$ cat .claude/idea-to-design/security-scan/security/security-summary-*.md

# 3. Fix critical/high issues
$ # ... make fixes ...

# 4. Re-scan to verify
$ npm run security:scan

✅ No critical or high severity findings

# 5. Create backlog for remaining issues
$ node scripts/backlog-sync.js --session-dir .claude/idea-to-design/security-scan
```

---

## FAQ

**Q: How often should I run security scans?**
A: On every commit (via CI/CD), before PR submission, and weekly for full codebase.

**Q: What if I get too many false positives?**
A: Configure exclusions in `.semgrep.yml` or `.bandit` config files.

**Q: Can I add custom rules?**
A: Yes! Both Semgrep and Bandit support custom rules. See Rulesets section.

**Q: How do I prioritize fixes?**
A: Critical → High → Medium → Low. Focus on exploitability and impact.

**Q: What about dependency vulnerabilities?**
A: Use `npm audit` for Node.js and `pip-audit` for Python dependencies separately.

**Q: Can I integrate with other tools?**
A: Yes! The JSON reports can be consumed by SIEM, SOAR, or bug tracking systems.

---

**Last Updated**: October 2024
**Next Review**: January 2025
