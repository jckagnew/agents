import { defineConfig } from 'vitest/config'
import { resolve } from 'path'

export default defineConfig({
  test: {
    // Test environment
    environment: 'node',
    
    // Test file patterns
    include: [
      'tests/unit/**/*.{test,spec}.{js,ts,jsx,tsx}',
      'src/**/*.{test,spec}.{js,ts,jsx,tsx}',
      'scripts/**/*.{test,spec}.{js,ts,jsx,tsx}'
    ],
    
    // Exclude patterns
    exclude: [
      'node_modules/**',
      'dist/**',
      'build/**',
      '.next/**',
      'coverage/**',
      'tests/integration/**',
      'tests/e2e/**'
    ],
    
    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      reportsDirectory: './coverage/unit',
      include: [
        'src/**/*.{js,ts,jsx,tsx}',
        'scripts/**/*.{js,ts,jsx,tsx}'
      ],
      exclude: [
        'src/**/*.{test,spec}.{js,ts,jsx,tsx}',
        'scripts/**/*.{test,spec}.{js,ts,jsx,tsx}',
        'src/**/*.d.ts',
        'src/**/types/**',
        'src/**/__mocks__/**'
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    },
    
    // Test timeout
    testTimeout: 10000,
    
    // Setup files
    setupFiles: [
      './tests/setup/unit-setup.ts'
    ],
    
    // Global test configuration
    globals: true,
    
    // Reporter configuration
    reporter: ['verbose', 'json', 'html'],
    outputFile: {
      json: './reports/unit-test-results.json',
      html: './reports/unit-test-report.html'
    },
    
    // Watch mode configuration
    watch: false,
    
    // Parallel execution
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false
      }
    }
  },
  
  // Resolve configuration
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@tests': resolve(__dirname, './tests'),
      '@scripts': resolve(__dirname, './scripts'),
      '@config': resolve(__dirname, './config')
    }
  },
  
  // Define global constants
  define: {
    'import.meta.vitest': 'undefined'
  }
})