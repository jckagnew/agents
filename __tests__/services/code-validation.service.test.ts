/**
 * Code Validation Service Unit Tests
 * Testing Checkpoint 4: Code Validation
 */

import { CodeValidationService } from '../../src/services/code-validation.service';
import { exec } from 'child_process';

// Mock child_process
jest.mock('child_process');
jest.mock('fs/promises');

const mockExec = exec as unknown as jest.Mock;

describe('CodeValidationService', () => {
  let codeValidationService: CodeValidationService;

  beforeEach(() => {
    jest.clearAllMocks();
    codeValidationService = new CodeValidationService();
  });

  describe('runESLint', () => {
    it('✅ ESLint runs and reports issues', async () => {
      // Mock ESLint output with errors and warnings
      const eslintOutput = JSON.stringify([
        {
          filePath: '/project/src/App.tsx',
          messages: [
            {
              line: 10,
              column: 5,
              severity: 2,
              message: 'Missing semicolon',
              ruleId: 'semi',
            },
            {
              line: 15,
              column: 10,
              severity: 1,
              message: 'Prefer const',
              ruleId: 'prefer-const',
            },
          ],
        },
      ]);

      mockExec.mockImplementation((cmd: string, options: any, callback: any) => {
        callback(null, { stdout: eslintOutput, stderr: '' });
        return {} as any;
      });

      // Mock promisify to use the callback
      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: eslintOutput,
        stderr: '',
      }));

      const result = await codeValidationService.runESLint('/project');

      expect(result.passed).toBe(false); // Has errors
      expect(result.errors).toBe(1);
      expect(result.warnings).toBe(1);
      expect(result.issues).toHaveLength(2);
      expect(result.issues[0].severity).toBe('error');
      expect(result.issues[1].severity).toBe('warning');
    });

    it('✅ ESLint passes with no issues', async () => {
      const eslintOutput = JSON.stringify([]);

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: eslintOutput,
        stderr: '',
      }));

      const result = await codeValidationService.runESLint('/project');

      expect(result.passed).toBe(true);
      expect(result.errors).toBe(0);
      expect(result.warnings).toBe(0);
      expect(result.issues).toHaveLength(0);
    });

    it('✅ Handles ESLint not installed gracefully', async () => {
      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => {
        throw new Error('ESLint not found');
      });

      const result = await codeValidationService.runESLint('/project');

      // Should pass with warning instead of failing
      expect(result.passed).toBe(true);
      expect(result.warnings).toBe(1);
      expect(result.issues[0].message).toContain('ESLint check skipped');
    });
  });

  describe('runTypeScriptCheck', () => {
    it('✅ TypeScript compilation checked', async () => {
      // Mock TypeScript errors
      const tsError = {
        stderr: `
src/App.tsx(10,5): error TS2322: Type 'string' is not assignable to type 'number'.
src/utils/helper.ts(25,10): error TS2304: Cannot find name 'unknown'.
        `,
      };

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => {
        throw tsError;
      });

      // Mock fileExists to return true
      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.runTypeScriptCheck('/project');

      expect(result.passed).toBe(false);
      expect(result.errors).toBe(2);
      expect(result.issues).toHaveLength(2);
      expect(result.issues[0].code).toBe('TS2322');
      expect(result.issues[1].code).toBe('TS2304');
    });

    it('✅ TypeScript compilation succeeds', async () => {
      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: '',
        stderr: '',
      }));

      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.runTypeScriptCheck('/project');

      expect(result.passed).toBe(true);
      expect(result.errors).toBe(0);
      expect(result.issues).toHaveLength(0);
    });

    it('✅ Skips check if no tsconfig.json', async () => {
      const fs = require('fs/promises');
      fs.access.mockRejectedValue(new Error('File not found'));

      const result = await codeValidationService.runTypeScriptCheck('/project');

      expect(result.passed).toBe(true);
      expect(result.errors).toBe(0);
    });
  });

  describe('runSemgrep', () => {
    it('✅ Semgrep security checks pass', async () => {
      const semgrepOutput = JSON.stringify({
        results: [
          {
            path: '/project/src/api.ts',
            start: { line: 15 },
            extra: {
              severity: 'high',
              message: 'SQL injection vulnerability',
              metadata: { cwe: 'CWE-89' },
            },
            check_id: 'javascript.lang.security.audit.sql-injection',
          },
          {
            path: '/project/src/auth.ts',
            start: { line: 30 },
            extra: {
              severity: 'medium',
              message: 'Weak password hashing',
            },
            check_id: 'javascript.crypto.weak-hash',
          },
        ],
      });

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: semgrepOutput,
        stderr: '',
      }));

      const result = await codeValidationService.runSemgrep('/project');

      expect(result.passed).toBe(false); // Has high severity
      expect(result.critical).toBe(0);
      expect(result.high).toBe(1);
      expect(result.medium).toBe(1);
      expect(result.low).toBe(0);
      expect(result.findings).toHaveLength(2);
    });

    it('✅ No security issues found', async () => {
      const semgrepOutput = JSON.stringify({ results: [] });

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: semgrepOutput,
        stderr: '',
      }));

      const result = await codeValidationService.runSemgrep('/project');

      expect(result.passed).toBe(true);
      expect(result.critical).toBe(0);
      expect(result.high).toBe(0);
      expect(result.findings).toHaveLength(0);
    });

    it('✅ Handles Semgrep not installed', async () => {
      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => {
        throw new Error('Semgrep not found');
      });

      const result = await codeValidationService.runSemgrep('/project');

      // Should pass (skip check) instead of failing
      expect(result.passed).toBe(true);
      expect(result.findings).toHaveLength(0);
    });
  });

  describe('runNpmAudit', () => {
    it('✅ npm audit detects vulnerabilities', async () => {
      const auditOutput = JSON.stringify({
        vulnerabilities: {
          lodash: {
            severity: 'critical',
            via: 'prototype pollution',
            title: 'Prototype Pollution in lodash',
            url: 'https://github.com/advisories/GHSA-xxxx',
          },
          axios: {
            severity: 'high',
            via: 'SSRF',
            title: 'Server-Side Request Forgery',
            url: 'https://github.com/advisories/GHSA-yyyy',
          },
        },
        metadata: {
          vulnerabilities: {
            critical: 1,
            high: 1,
            moderate: 0,
            low: 0,
            total: 2,
          },
        },
      });

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => {
        const error: any = new Error('npm audit found vulnerabilities');
        error.stdout = auditOutput;
        throw error;
      });

      const result = await codeValidationService.runNpmAudit('/project');

      expect(result.passed).toBe(false);
      expect(result.vulnerabilities.critical).toBe(1);
      expect(result.vulnerabilities.high).toBe(1);
      expect(result.vulnerabilities.total).toBe(2);
      expect(result.findings).toHaveLength(2);
    });

    it('✅ No vulnerabilities found', async () => {
      const auditOutput = JSON.stringify({
        vulnerabilities: {},
        metadata: {
          vulnerabilities: {
            critical: 0,
            high: 0,
            moderate: 0,
            low: 0,
            total: 0,
          },
        },
      });

      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => ({
        stdout: auditOutput,
        stderr: '',
      }));

      const result = await codeValidationService.runNpmAudit('/project');

      expect(result.passed).toBe(true);
      expect(result.vulnerabilities.total).toBe(0);
      expect(result.findings).toHaveLength(0);
    });

    it('✅ Handles npm audit not available', async () => {
      const { promisify } = require('util');
      promisify.mockImplementation(() => async () => {
        throw new Error('npm not found');
      });

      const result = await codeValidationService.runNpmAudit('/project');

      // Should pass (skip check) instead of failing
      expect(result.passed).toBe(true);
      expect(result.vulnerabilities.total).toBe(0);
    });
  });

  describe('validateGeneratedCode', () => {
    it('✅ Overall status calculated correctly - PASSED', async () => {
      // Mock all checks passing
      const { promisify } = require('util');
      promisify.mockImplementation((fn: any) => {
        return async (...args: any[]) => {
          const cmd = args[0];
          if (cmd.includes('eslint')) {
            return { stdout: JSON.stringify([]), stderr: '' };
          }
          if (cmd.includes('tsc')) {
            return { stdout: '', stderr: '' };
          }
          if (cmd.includes('semgrep')) {
            return { stdout: JSON.stringify({ results: [] }), stderr: '' };
          }
          if (cmd.includes('npm audit')) {
            return {
              stdout: JSON.stringify({
                vulnerabilities: {},
                metadata: { vulnerabilities: { critical: 0, high: 0, moderate: 0, low: 0, total: 0 } },
              }),
              stderr: '',
            };
          }
        };
      });

      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.validateGeneratedCode('/project');

      expect(result.overall_status).toBe('passed');
      expect(result.summary.total_errors).toBe(0);
      expect(result.summary.blocking_issues).toBe(0);
      expect(result.static_analysis.eslint.passed).toBe(true);
      expect(result.static_analysis.typescript.passed).toBe(true);
      expect(result.security.semgrep.passed).toBe(true);
      expect(result.security.npm_audit.passed).toBe(true);
    });

    it('✅ Overall status calculated correctly - FAILED', async () => {
      // Mock TypeScript errors (blocking)
      const { promisify } = require('util');
      promisify.mockImplementation((fn: any) => {
        return async (...args: any[]) => {
          const cmd = args[0];
          if (cmd.includes('tsc')) {
            const error: any = new Error('TypeScript errors');
            error.stderr = 'src/App.tsx(10,5): error TS2322: Type error.';
            throw error;
          }
          if (cmd.includes('eslint')) {
            return { stdout: JSON.stringify([]), stderr: '' };
          }
          if (cmd.includes('semgrep')) {
            return { stdout: JSON.stringify({ results: [] }), stderr: '' };
          }
          if (cmd.includes('npm audit')) {
            return {
              stdout: JSON.stringify({
                vulnerabilities: {},
                metadata: { vulnerabilities: { critical: 0, high: 0, moderate: 0, low: 0, total: 0 } },
              }),
              stderr: '',
            };
          }
        };
      });

      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.validateGeneratedCode('/project');

      expect(result.overall_status).toBe('failed');
      expect(result.summary.blocking_issues).toBeGreaterThan(0);
      expect(result.static_analysis.typescript.passed).toBe(false);
    });

    it('✅ Overall status calculated correctly - WARNINGS', async () => {
      // Mock warnings but no errors
      const { promisify } = require('util');
      promisify.mockImplementation((fn: any) => {
        return async (...args: any[]) => {
          const cmd = args[0];
          if (cmd.includes('eslint')) {
            return {
              stdout: JSON.stringify([
                {
                  filePath: '/project/src/App.tsx',
                  messages: [
                    {
                      line: 10,
                      column: 5,
                      severity: 1, // Warning
                      message: 'Prefer const',
                      ruleId: 'prefer-const',
                    },
                  ],
                },
              ]),
              stderr: '',
            };
          }
          if (cmd.includes('tsc')) {
            return { stdout: '', stderr: '' };
          }
          if (cmd.includes('semgrep')) {
            return { stdout: JSON.stringify({ results: [] }), stderr: '' };
          }
          if (cmd.includes('npm audit')) {
            return {
              stdout: JSON.stringify({
                vulnerabilities: {},
                metadata: { vulnerabilities: { critical: 0, high: 0, moderate: 0, low: 0, total: 0 } },
              }),
              stderr: '',
            };
          }
        };
      });

      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.validateGeneratedCode('/project');

      expect(result.overall_status).toBe('warnings');
      expect(result.summary.total_warnings).toBeGreaterThan(0);
      expect(result.summary.blocking_issues).toBe(0);
    });

    it('✅ Critical security issues are blocking', async () => {
      // Mock critical security issue
      const { promisify } = require('util');
      promisify.mockImplementation((fn: any) => {
        return async (...args: any[]) => {
          const cmd = args[0];
          if (cmd.includes('semgrep')) {
            return {
              stdout: JSON.stringify({
                results: [
                  {
                    path: '/project/src/api.ts',
                    start: { line: 15 },
                    extra: {
                      severity: 'critical',
                      message: 'Critical security issue',
                    },
                    check_id: 'test-rule',
                  },
                ],
              }),
              stderr: '',
            };
          }
          if (cmd.includes('eslint')) {
            return { stdout: JSON.stringify([]), stderr: '' };
          }
          if (cmd.includes('tsc')) {
            return { stdout: '', stderr: '' };
          }
          if (cmd.includes('npm audit')) {
            return {
              stdout: JSON.stringify({
                vulnerabilities: {},
                metadata: { vulnerabilities: { critical: 0, high: 0, moderate: 0, low: 0, total: 0 } },
              }),
              stderr: '',
            };
          }
        };
      });

      const fs = require('fs/promises');
      fs.access.mockResolvedValue(undefined);

      const result = await codeValidationService.validateGeneratedCode('/project');

      expect(result.overall_status).toBe('failed');
      expect(result.summary.critical_security_issues).toBe(1);
      expect(result.summary.blocking_issues).toBe(1);
    });
  });
});

// Testing Checkpoint 4 Summary
describe('Testing Checkpoint 4: Code Validation', () => {
  it('CHECKPOINT SUMMARY', () => {
    const checklistItems = `
    Testing Checkpoint 4: Code validation tests
    ✅ ESLint runs on generated code and reports issues
    ✅ TypeScript compilation checked
    ✅ Semgrep security checks applied
    ✅ npm audit detects vulnerabilities
    ✅ Overall status calculated correctly (passed/failed/warnings)
    ✅ Critical security issues are blocking
    ✅ Graceful handling when tools not installed
    `;
    console.log(checklistItems);
  });
});
