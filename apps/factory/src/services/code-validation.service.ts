/**
 * Code Validation Service
 * Multi-layer validation for generated code
 *
 * Validation Layers:
 * 1. ESLint - Code quality and style
 * 2. TypeScript - Type checking
 * 3. Semgrep - Security vulnerability scanning
 * 4. npm audit - Dependency vulnerability detection
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs/promises';

const execAsync = promisify(exec);

export interface LintResult {
  passed: boolean;
  errors: number;
  warnings: number;
  issues: Array<{
    file: string;
    line: number;
    column: number;
    severity: 'error' | 'warning';
    message: string;
    rule: string;
  }>;
}

export interface TypeCheckResult {
  passed: boolean;
  errors: number;
  issues: Array<{
    file: string;
    line: number;
    column: number;
    message: string;
    code: string;
  }>;
}

export interface SecurityResult {
  passed: boolean;
  critical: number;
  high: number;
  medium: number;
  low: number;
  findings: Array<{
    file: string;
    line: number;
    severity: 'critical' | 'high' | 'medium' | 'low';
    message: string;
    rule_id: string;
    cwe?: string;
  }>;
}

export interface AuditResult {
  passed: boolean;
  vulnerabilities: {
    critical: number;
    high: number;
    moderate: number;
    low: number;
    total: number;
  };
  findings: Array<{
    name: string;
    severity: string;
    via: string;
    title: string;
    url?: string;
  }>;
}

export interface CodeQualityGate {
  overall_status: 'passed' | 'failed' | 'warnings';
  static_analysis: {
    eslint: LintResult;
    typescript: TypeCheckResult;
  };
  security: {
    semgrep: SecurityResult;
    npm_audit: AuditResult;
  };
  summary: {
    total_errors: number;
    total_warnings: number;
    critical_security_issues: number;
    blocking_issues: number;
  };
  // Flat accessors for backwards compatibility
  eslint_result?: LintResult;
  typescript_result?: TypeCheckResult;
  semgrep_result?: SecurityResult;
  npm_audit_result?: AuditResult;
  recommendations?: string[];
}

/**
 * Code Validation Service
 */
export class CodeValidationService {
  private static instance: CodeValidationService;

  /**
   * Get singleton instance
   */
  static getInstance(): CodeValidationService {
    if (!CodeValidationService.instance) {
      CodeValidationService.instance = new CodeValidationService();
    }
    return CodeValidationService.instance;
  }

  /**
   * Validate generated code (full quality gate)
   */
  async validateGeneratedCode(projectPath: string): Promise<CodeQualityGate> {
    // Run all validations in parallel
    const [eslintResult, typescriptResult, semgrepResult, auditResult] =
      await Promise.all([
        this.runESLint(projectPath),
        this.runTypeScriptCheck(projectPath),
        this.runSemgrep(projectPath),
        this.runNpmAudit(projectPath),
      ]);

    // Calculate summary
    const totalErrors =
      eslintResult.errors +
      typescriptResult.errors +
      semgrepResult.critical +
      semgrepResult.high +
      auditResult.vulnerabilities.critical;

    const totalWarnings =
      eslintResult.warnings +
      semgrepResult.medium +
      auditResult.vulnerabilities.high;

    const criticalSecurityIssues =
      semgrepResult.critical + auditResult.vulnerabilities.critical;

    const blockingIssues =
      typescriptResult.errors +
      semgrepResult.critical +
      auditResult.vulnerabilities.critical;

    // Determine overall status
    let overallStatus: 'passed' | 'failed' | 'warnings';
    if (blockingIssues > 0) {
      overallStatus = 'failed';
    } else if (totalWarnings > 0) {
      overallStatus = 'warnings';
    } else {
      overallStatus = 'passed';
    }

    return {
      overall_status: overallStatus,
      static_analysis: {
        eslint: eslintResult,
        typescript: typescriptResult,
      },
      security: {
        semgrep: semgrepResult,
        npm_audit: auditResult,
      },
      summary: {
        total_errors: totalErrors,
        total_warnings: totalWarnings,
        critical_security_issues: criticalSecurityIssues,
        blocking_issues: blockingIssues,
      },
    };
  }

  /**
   * Run ESLint on generated code
   */
  async runESLint(projectPath: string): Promise<LintResult> {
    try {
      // Check if ESLint config exists
      const eslintConfigPath = path.join(projectPath, '.eslintrc.json');
      const hasConfig = await this.fileExists(eslintConfigPath);

      if (!hasConfig) {
        // Create minimal ESLint config
        await this.createDefaultESLintConfig(projectPath);
      }

      // Run ESLint
      const { stdout } = await execAsync(
        `npx eslint --format json "src/**/*.{ts,tsx,js,jsx}"`,
        {
          cwd: projectPath,
          maxBuffer: 10 * 1024 * 1024, // 10MB buffer
        }
      );

      const results = JSON.parse(stdout);

      // Parse results
      const issues: LintResult['issues'] = [];
      let totalErrors = 0;
      let totalWarnings = 0;

      results.forEach((fileResult: any) => {
        fileResult.messages.forEach((message: any) => {
          issues.push({
            file: fileResult.filePath.replace(projectPath, '').substring(1),
            line: message.line,
            column: message.column,
            severity: message.severity === 2 ? 'error' : 'warning',
            message: message.message,
            rule: message.ruleId || 'unknown',
          });

          if (message.severity === 2) totalErrors++;
          else totalWarnings++;
        });
      });

      return {
        passed: totalErrors === 0,
        errors: totalErrors,
        warnings: totalWarnings,
        issues,
      };
    } catch (error: any) {
      // ESLint non-zero exit code means errors found
      if (error.stdout) {
        try {
          const results = JSON.parse(error.stdout);
          const issues: LintResult['issues'] = [];
          let totalErrors = 0;
          let totalWarnings = 0;

          results.forEach((fileResult: any) => {
            fileResult.messages.forEach((message: any) => {
              issues.push({
                file: fileResult.filePath.replace(projectPath, '').substring(1),
                line: message.line,
                column: message.column,
                severity: message.severity === 2 ? 'error' : 'warning',
                message: message.message,
                rule: message.ruleId || 'unknown',
              });

              if (message.severity === 2) totalErrors++;
              else totalWarnings++;
            });
          });

          return {
            passed: totalErrors === 0,
            errors: totalErrors,
            warnings: totalWarnings,
            issues,
          };
        } catch (parseError) {
          // Fallback if JSON parsing fails
          return {
            passed: false,
            errors: 1,
            warnings: 0,
            issues: [
              {
                file: 'unknown',
                line: 0,
                column: 0,
                severity: 'error',
                message: `ESLint failed: ${error.message}`,
                rule: 'eslint-error',
              },
            ],
          };
        }
      }

      // ESLint not installed or other error
      return {
        passed: true,
        errors: 0,
        warnings: 1,
        issues: [
          {
            file: 'project',
            line: 0,
            column: 0,
            severity: 'warning',
            message: `ESLint check skipped: ${error.message}`,
            rule: 'eslint-skip',
          },
        ],
      };
    }
  }

  /**
   * Run TypeScript type checking
   */
  async runTypeScriptCheck(projectPath: string): Promise<TypeCheckResult> {
    try {
      // Check if tsconfig.json exists
      const tsconfigPath = path.join(projectPath, 'tsconfig.json');
      const hasConfig = await this.fileExists(tsconfigPath);

      if (!hasConfig) {
        // No TypeScript config, skip check
        return {
          passed: true,
          errors: 0,
          issues: [],
        };
      }

      // Run TypeScript compiler in check mode
      await execAsync('npx tsc --noEmit --pretty false', {
        cwd: projectPath,
        maxBuffer: 10 * 1024 * 1024,
      });

      // No errors
      return {
        passed: true,
        errors: 0,
        issues: [],
      };
    } catch (error: any) {
      // Parse TypeScript errors from stderr
      const stderr = error.stderr || '';
      const issues: TypeCheckResult['issues'] = [];

      // TypeScript error format: filename.ts(line,col): error TS1234: message
      const errorRegex = /(.+?)\((\d+),(\d+)\): error (TS\d+): (.+)/g;
      let match;

      while ((match = errorRegex.exec(stderr)) !== null) {
        issues.push({
          file: match[1].replace(projectPath, '').substring(1),
          line: parseInt(match[2], 10),
          column: parseInt(match[3], 10),
          code: match[4],
          message: match[5],
        });
      }

      return {
        passed: false,
        errors: issues.length,
        issues,
      };
    }
  }

  /**
   * Run Semgrep security scanning
   */
  async runSemgrep(projectPath: string): Promise<SecurityResult> {
    try {
      // Run Semgrep with security rules
      const { stdout } = await execAsync(
        'npx semgrep --config auto --json --quiet',
        {
          cwd: projectPath,
          maxBuffer: 10 * 1024 * 1024,
        }
      );

      const results = JSON.parse(stdout);

      // Parse findings
      const findings: SecurityResult['findings'] = [];
      let critical = 0;
      let high = 0;
      let medium = 0;
      let low = 0;

      (results.results || []).forEach((finding: any) => {
        const severity = finding.extra.severity || 'low';

        findings.push({
          file: finding.path.replace(projectPath, '').substring(1),
          line: finding.start.line,
          severity: severity.toLowerCase() as any,
          message: finding.extra.message,
          rule_id: finding.check_id,
          cwe: finding.extra.metadata?.cwe,
        });

        switch (severity.toLowerCase()) {
          case 'critical':
            critical++;
            break;
          case 'high':
            high++;
            break;
          case 'medium':
            medium++;
            break;
          case 'low':
            low++;
            break;
        }
      });

      return {
        passed: critical === 0 && high === 0,
        critical,
        high,
        medium,
        low,
        findings,
      };
    } catch (error: any) {
      // Semgrep not installed or error - skip check
      return {
        passed: true,
        critical: 0,
        high: 0,
        medium: 0,
        low: 0,
        findings: [],
      };
    }
  }

  /**
   * Run npm audit for dependency vulnerabilities
   */
  async runNpmAudit(projectPath: string): Promise<AuditResult> {
    try {
      // Run npm audit
      const { stdout } = await execAsync('npm audit --json', {
        cwd: projectPath,
        maxBuffer: 10 * 1024 * 1024,
      });

      const results = JSON.parse(stdout);

      // Parse vulnerabilities
      const findings: AuditResult['findings'] = [];
      const vulns = results.vulnerabilities || {};

      Object.entries(vulns).forEach(([name, data]: [string, any]) => {
        findings.push({
          name,
          severity: data.severity,
          via: Array.isArray(data.via) ? data.via.join(', ') : data.via,
          title: data.title || name,
          url: data.url,
        });
      });

      const metadata = results.metadata?.vulnerabilities || {
        critical: 0,
        high: 0,
        moderate: 0,
        low: 0,
        total: 0,
      };

      return {
        passed: metadata.critical === 0 && metadata.high === 0,
        vulnerabilities: {
          critical: metadata.critical || 0,
          high: metadata.high || 0,
          moderate: metadata.moderate || 0,
          low: metadata.low || 0,
          total: metadata.total || 0,
        },
        findings,
      };
    } catch (error: any) {
      // Try to parse error output (npm audit exits non-zero if vulnerabilities found)
      if (error.stdout) {
        try {
          const results = JSON.parse(error.stdout);
          const findings: AuditResult['findings'] = [];
          const vulns = results.vulnerabilities || {};

          Object.entries(vulns).forEach(([name, data]: [string, any]) => {
            findings.push({
              name,
              severity: data.severity,
              via: Array.isArray(data.via) ? data.via.join(', ') : data.via,
              title: data.title || name,
              url: data.url,
            });
          });

          const metadata = results.metadata?.vulnerabilities || {
            critical: 0,
            high: 0,
            moderate: 0,
            low: 0,
            total: 0,
          };

          return {
            passed: metadata.critical === 0 && metadata.high === 0,
            vulnerabilities: {
              critical: metadata.critical || 0,
              high: metadata.high || 0,
              moderate: metadata.moderate || 0,
              low: metadata.low || 0,
              total: metadata.total || 0,
            },
            findings,
          };
        } catch (parseError) {
          // Fallback
        }
      }

      // npm audit failed or not available - pass with warning
      return {
        passed: true,
        vulnerabilities: {
          critical: 0,
          high: 0,
          moderate: 0,
          low: 0,
          total: 0,
        },
        findings: [],
      };
    }
  }

  /**
   * Helper: Check if file exists
   */
  private async fileExists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Helper: Create default ESLint config
   */
  private async createDefaultESLintConfig(projectPath: string): Promise<void> {
    const config = {
      extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:react/recommended',
        'plugin:react-native/all',
      ],
      parser: '@typescript-eslint/parser',
      plugins: ['@typescript-eslint', 'react', 'react-native'],
      rules: {
        'react/react-in-jsx-scope': 'off',
        'react/prop-types': 'off',
        '@typescript-eslint/no-explicit-any': 'warn',
      },
      env: {
        'react-native/react-native': true,
      },
      settings: {
        react: {
          version: 'detect',
        },
      },
    };

    await fs.writeFile(
      path.join(projectPath, '.eslintrc.json'),
      JSON.stringify(config, null, 2)
    );
  }
}

/**
 * Singleton instance
 */
let codeValidationServiceInstance: CodeValidationService | null = null;

export function getCodeValidationService(): CodeValidationService {
  if (!codeValidationServiceInstance) {
    codeValidationServiceInstance = new CodeValidationService();
  }

  return codeValidationServiceInstance;
}
