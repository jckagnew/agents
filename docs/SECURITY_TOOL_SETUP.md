# Security Tool Setup Guide

## Overview

This guide explains how to set up and configure security scanning tools for the Software Factory pipeline, including Semgrep and Bandit.

## Prerequisites

- macOS with Homebrew installed
- Python 3.8+ (for Bandit)
- Node.js 18+ (for JavaScript/TypeScript scanning)
- Git repository with code to scan

## Tool Installation

### 1. Semgrep Installation

Semgrep is a static analysis tool that finds bugs and security issues in code.

```bash
# Install via Homebrew (recommended)
brew install semgrep

# Verify installation
semgrep --version
```

**Alternative Installation Methods:**
```bash
# Install via pip (if Homebrew not available)
pip install semgrep

# Install via Docker
docker pull returntocorp/semgrep
```

### 2. Bandit Installation

Bandit is a security linter for Python code.

```bash
# Install via Homebrew (recommended)
brew install bandit

# Verify installation
bandit --version
```

**Alternative Installation Methods:**
```bash
# Install via pip (if Homebrew not available)
pip install bandit

# Install via Docker
docker pull pyupio/bandit
```

## Configuration Files

### 1. Semgrep Configuration

**File**: `config/security/.semgrep.yml`

This configuration includes:
- **OWASP Top 10 Rules**: SQL injection, XSS, command injection
- **Authentication Security**: Hardcoded secrets, weak crypto, missing auth
- **Data Validation**: Input validation, path traversal
- **Error Handling**: Sensitive data logging, error exposure
- **Framework-Specific**: Next.js, React, Supabase security patterns

**Key Features**:
- Multi-language support (JavaScript, TypeScript, Python, Java, C#)
- Severity levels (ERROR, WARNING, INFO)
- Exclude patterns for build artifacts and test files
- JSON output format for CI/CD integration

### 2. Bandit Configuration

**File**: `config/security/bandit.ini`

This configuration includes:
- **Severity Levels**: LOW, MEDIUM, HIGH, CRITICAL
- **Confidence Levels**: LOW, MEDIUM, HIGH
- **Exclude Patterns**: Build artifacts, test files, virtual environments
- **Output Format**: JSON for CI/CD integration

## Local Usage

### 1. Basic Semgrep Scanning

```bash
# Scan current directory with default rules
semgrep --config=config/security/.semgrep.yml .

# Scan specific directory
semgrep --config=config/security/.semgrep.yml src/

# Scan with custom output
semgrep --config=config/security/.semgrep.yml --json --output=reports/semgrep-report.json .

# Scan specific file types
semgrep --config=config/security/.semgrep.yml --include="*.js,*.ts,*.jsx,*.tsx" .
```

### 2. Basic Bandit Scanning

```bash
# Scan Python files in current directory
bandit -r . -f json -o reports/bandit-report.json

# Scan with custom config
bandit -r . -c config/security/bandit.ini

# Scan specific directory
bandit -r src/ -f json -o reports/bandit-report.json

# Scan with severity filter
bandit -r . -ll -f json -o reports/bandit-report.json
```

### 3. Combined Security Scan

```bash
# Create reports directory
mkdir -p reports

# Run Semgrep scan
semgrep --config=config/security/.semgrep.yml --json --output=reports/semgrep-report.json .

# Run Bandit scan
bandit -r . -f json -o reports/bandit-report.json

# View results
cat reports/semgrep-report.json | jq '.results[] | {rule_id, severity, message, path}'
cat reports/bandit-report.json | jq '.results[] | {test_id, severity, confidence, issue_text, filename}'
```

## Rule Configuration

### 1. Customizing Semgrep Rules

**Adding New Rules**:
```yaml
# Add to config/security/.semgrep.yml
rules:
  - id: custom-rule
    message: "Custom security rule description"
    languages: [javascript, typescript]
    severity: ERROR
    patterns:
      - pattern: |
          $DANGEROUS_FUNCTION($USER_INPUT)
```

**Excluding False Positives**:
```yaml
# Add to exclude section
exclude:
  - "src/legacy/**"  # Exclude legacy code
  - "**/*.test.js"   # Exclude test files
  - "**/vendor/**"   # Exclude third-party code
```

### 2. Customizing Bandit Rules

**Skipping Specific Tests**:
```ini
# Add to config/security/bandit.ini
skip = B101,B601,B603  # Skip specific test IDs
```

**Excluding Files**:
```ini
# Add to config/security/bandit.ini
exclude = *.pyc,*.pyo,__pycache__,*.test.py
```

## Integration with Software Factory

### 1. NPM Scripts

Add to `package.json`:
```json
{
  "scripts": {
    "security:scan": "npm run security:semgrep && npm run security:bandit",
    "security:semgrep": "semgrep --config=config/security/.semgrep.yml --json --output=reports/semgrep-report.json .",
    "security:bandit": "bandit -r . -f json -o reports/bandit-report.json",
    "security:report": "node scripts/security-report.js"
  }
}
```

### 2. Security Report Script

Create `scripts/security-report.js`:
```javascript
const fs = require('fs');
const path = require('path');

function generateSecurityReport() {
    const semgrepReport = JSON.parse(fs.readFileSync('reports/semgrep-report.json', 'utf8'));
    const banditReport = JSON.parse(fs.readFileSync('reports/bandit-report.json', 'utf8'));
    
    const report = {
        timestamp: new Date().toISOString(),
        semgrep: {
            findings: semgrepReport.results.length,
            errors: semgrepReport.results.filter(r => r.level === 'ERROR').length,
            warnings: semgrepReport.results.filter(r => r.level === 'WARNING').length
        },
        bandit: {
            findings: banditReport.results.length,
            high: banditReport.results.filter(r => r.issue_severity === 'HIGH').length,
            medium: banditReport.results.filter(r => r.issue_severity === 'MEDIUM').length
        }
    };
    
    fs.writeFileSync('reports/security-summary.json', JSON.stringify(report, null, 2));
    console.log('Security report generated:', report);
}

generateSecurityReport();
```

## CI/CD Integration

### 1. GitHub Actions

Add to `.github/workflows/security.yml`:
```yaml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install Semgrep
        run: |
          curl -L https://github.com/returntocorp/semgrep/releases/latest/download/semgrep-v1.140.0-osx-x86_64.tar.gz | tar -xz
          sudo mv semgrep /usr/local/bin/
          
      - name: Install Bandit
        run: |
          pip install bandit
          
      - name: Run Semgrep Scan
        run: |
          semgrep --config=config/security/.semgrep.yml --json --output=reports/semgrep-report.json .
          
      - name: Run Bandit Scan
        run: |
          bandit -r . -f json -o reports/bandit-report.json
          
      - name: Upload Security Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: reports/
```

### 2. Pre-commit Hooks

Install pre-commit hooks:
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: local
    hooks:
      - id: semgrep
        name: semgrep
        entry: semgrep --config=config/security/.semgrep.yml
        language: system
        files: \.(js|ts|jsx|tsx|py|java|cs)$
        
      - id: bandit
        name: bandit
        entry: bandit -r
        language: system
        files: \.py$
EOF

# Install hooks
pre-commit install
```

## Troubleshooting

### Common Issues

#### Semgrep Issues
```bash
# Configuration not found
semgrep --config=config/security/.semgrep.yml .
# Error: Could not find config file
# Solution: Ensure config file exists and path is correct

# No findings reported
semgrep --config=config/security/.semgrep.yml --verbose .
# Solution: Check if files match language patterns in config

# Performance issues
semgrep --config=config/security/.semgrep.yml --max-target-bytes=1000000 .
# Solution: Increase max-target-bytes or exclude large files
```

#### Bandit Issues
```bash
# No Python files found
bandit -r . -f json
# Error: No files to scan
# Solution: Ensure Python files exist in target directory

# Configuration errors
bandit -r . -c config/security/bandit.ini
# Error: Invalid configuration
# Solution: Check INI file syntax and test IDs

# Permission errors
bandit -r . -f json -o reports/bandit-report.json
# Error: Permission denied
# Solution: Ensure reports directory exists and is writable
```

### Performance Optimization

#### Semgrep Performance
```bash
# Exclude large directories
semgrep --config=config/security/.semgrep.yml --exclude="node_modules,dist,build" .

# Limit file size
semgrep --config=config/security/.semgrep.yml --max-target-bytes=1000000 .

# Use specific rules only
semgrep --config="p/owasp-top-ten" .
```

#### Bandit Performance
```bash
# Skip specific tests
bandit -r . -s B101,B601

# Limit severity levels
bandit -r . -ll  # Only LOW and MEDIUM severity

# Exclude directories
bandit -r . -x tests/,venv/,env/
```

## Best Practices

### 1. Regular Scanning
- Run security scans on every commit
- Schedule daily scans for critical repositories
- Include security scanning in CI/CD pipeline

### 2. Rule Management
- Review and update rules regularly
- Exclude false positives appropriately
- Add custom rules for project-specific patterns

### 3. Reporting
- Generate human-readable reports
- Track security metrics over time
- Alert on high-severity findings

### 4. Team Integration
- Train team on security best practices
- Review security findings in code reviews
- Establish security review process

## Next Steps

1. **Configure Rules**: Customize rules for your project needs
2. **Set Up CI/CD**: Integrate security scanning into your pipeline
3. **Monitor Results**: Track security metrics and trends
4. **Team Training**: Educate team on security best practices

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Use
