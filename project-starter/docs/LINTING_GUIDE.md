# 🎯 Comprehensive Linting Guide

## 📋 **Overview**

This guide covers the complete linting strategy for the project starter, ensuring code quality, consistency, and security across all supported technologies.

## 🛠️ **Linting Stack**

### **Python Linting**
- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting (profile: black)
- **flake8**: Style guide enforcement
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability checking

### **JavaScript/TypeScript Linting**
- **ESLint**: Code quality and style enforcement
- **Prettier**: Code formatting
- **TypeScript**: Type checking

### **Security Linting**
- **bandit**: Python security issues
- **safety**: Python dependency vulnerabilities
- **detect-secrets**: Secret detection
- **npm audit**: Node.js security audit

### **Documentation Linting**
- **Prettier**: Markdown formatting
- **YAML/JSON**: Syntax validation

## 🚀 **Quick Start**

### **Install Pre-commit Hooks**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### **Manual Linting Commands**

#### **Python Projects**
```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/

# Security checks
bandit -r src/
safety check
```

#### **JavaScript/TypeScript Projects**
```bash
# Lint and format
npm run lint
npm run lint:fix
npm run format

# Security audit
npm audit
npm audit fix
```

## 📁 **Configuration Files**

### **Python Configuration**
- `pyproject.toml`: Black, isort, mypy, pytest, coverage
- `.pre-commit-config.yaml`: Pre-commit hooks
- `requirements.txt`: Dependencies

### **JavaScript/TypeScript Configuration**
- `package.json`: ESLint, Prettier, Jest
- `.eslintrc.js`: ESLint rules
- `.prettierrc`: Prettier configuration

## 🎯 **Linting Rules by Technology**

### **Python Rules**
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
disallow_untyped_defs = true
```

### **JavaScript/TypeScript Rules**
```json
{
  "extends": ["eslint:recommended", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error",
    "no-console": "warn",
    "no-unused-vars": "error"
  }
}
```

## 🔧 **IDE Integration**

### **Cursor/VS Code**
1. Install recommended extensions:
   - Python (Microsoft)
   - ESLint
   - Prettier
   - Black Formatter
   - MyPy Type Checker

2. Add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### **Pre-commit Integration**
Pre-commit hooks run automatically on:
- `git commit`
- `git push`
- Manual execution

## 🚨 **Linting Failures**

### **Common Issues & Solutions**

#### **Black Formatting Issues**
```bash
# Auto-fix
black src/ tests/

# Check only
black --check src/ tests/
```

#### **ESLint Issues**
```bash
# Auto-fix
npm run lint:fix

# Check only
npm run lint
```

#### **MyPy Type Issues**
```bash
# Check types
mypy src/

# Ignore missing imports
mypy --ignore-missing-imports src/
```

## 📊 **Coverage Requirements**

### **Python Coverage**
- **Minimum**: 80% line coverage
- **Target**: 90% line coverage
- **Branches**: 80% coverage
- **Functions**: 80% coverage

### **JavaScript Coverage**
- **Minimum**: 80% line coverage
- **Branches**: 80% coverage
- **Functions**: 80% coverage
- **Statements**: 80% coverage

## 🔒 **Security Linting**

### **Python Security**
```bash
# Bandit security scan
bandit -r src/ -f json -o bandit-report.json

# Safety dependency check
safety check
```

### **JavaScript Security**
```bash
# NPM audit
npm audit
npm audit fix
```

### **Secret Detection**
```bash
# Detect secrets
detect-secrets scan --baseline .secrets.baseline
```

## 🎨 **Code Style Guidelines**

### **Python Style**
- **Line Length**: 88 characters (Black default)
- **Import Order**: isort with black profile
- **Type Hints**: Required for all functions
- **Docstrings**: Google style for all functions/classes

### **JavaScript/TypeScript Style**
- **Line Length**: 80 characters
- **Quotes**: Single quotes
- **Semicolons**: Required
- **Trailing Commas**: ES5 style

## 🚀 **Automation Scripts**

### **Lint All**
```bash
#!/bin/bash
# scripts/lint-all.sh

echo "🔍 Running Python linting..."
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
bandit -r src/

echo "🔍 Running JavaScript linting..."
npm run lint
npm run format

echo "🔍 Running security checks..."
npm audit
safety check

echo "✅ All linting completed!"
```

### **Pre-commit Setup**
```bash
#!/bin/bash
# scripts/setup-linting.sh

echo "🔧 Setting up linting..."

# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

echo "✅ Linting setup complete!"
```

## 📈 **Continuous Integration**

### **GitHub Actions Example**
```yaml
name: Linting

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Python dependencies
        run: pip install -r requirements.txt
      
      - name: Install Node dependencies
        run: npm install
      
      - name: Run Python linting
        run: |
          black --check src/ tests/
          isort --check-only src/ tests/
          flake8 src/ tests/
          mypy src/
          bandit -r src/
      
      - name: Run JavaScript linting
        run: |
          npm run lint
          npm run format:check
          npm audit
```

## 🎯 **Best Practices**

### **1. Lint Early, Lint Often**
- Run linting before every commit
- Fix issues immediately
- Don't accumulate technical debt

### **2. Configure Your IDE**
- Enable format on save
- Show linting errors in real-time
- Use consistent settings across team

### **3. Automate Everything**
- Use pre-commit hooks
- Integrate with CI/CD
- Set up automated fixes where possible

### **4. Document Standards**
- Keep this guide updated
- Document project-specific rules
- Train team members on standards

### **5. Gradual Adoption**
- Start with basic rules
- Gradually add stricter rules
- Use `# noqa` comments sparingly

## 🔧 **Troubleshooting**

### **Common Problems**

#### **Pre-commit Hooks Not Running**
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

#### **ESLint Configuration Issues**
```bash
# Check configuration
npx eslint --print-config src/index.js
```

#### **MyPy Import Errors**
```bash
# Install missing stubs
pip install types-requests types-PyYAML
```

## 📚 **Resources**

- [Black Documentation](https://black.readthedocs.io/)
- [ESLint Documentation](https://eslint.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)

## 🎉 **Conclusion**

This comprehensive linting strategy ensures:
- **Code Quality**: Consistent, readable code
- **Security**: Vulnerability detection and prevention
- **Maintainability**: Easy to understand and modify
- **Team Collaboration**: Shared standards and practices
- **Automation**: Minimal manual intervention required

Remember: **Good linting is not about perfection, it's about consistency and catching real issues before they become problems!**
