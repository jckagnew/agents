module.exports = {
  // =============================================================================
  // ESLINT CONFIGURATION
  // =============================================================================
  // Comprehensive ESLint configuration for JavaScript/TypeScript projects
  // =============================================================================

  // =============================================================================
  // PARSER CONFIGURATION
  // =============================================================================
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },

  // =============================================================================
  // ENVIRONMENT CONFIGURATION
  // =============================================================================
  env: {
    browser: true,
    node: true,
    es2022: true,
    jest: true,
  },

  // =============================================================================
  // EXTENDS CONFIGURATION
  // =============================================================================
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'prettier',
    'prettier/@typescript-eslint',
  ],

  // =============================================================================
  // PLUGINS CONFIGURATION
  // =============================================================================
  plugins: [
    '@typescript-eslint',
    'prettier',
    'import',
    'security',
    'jest',
  ],

  // =============================================================================
  // RULES CONFIGURATION
  // =============================================================================
  rules: {
    // =============================================================================
    // PRETTIER INTEGRATION
    // =============================================================================
    'prettier/prettier': 'error',

    // =============================================================================
    // TYPESCRIPT RULES
    // =============================================================================
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-inferrable-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'warn',
    '@typescript-eslint/prefer-const': 'error',
    '@typescript-eslint/no-var-requires': 'error',

    // =============================================================================
    // GENERAL JAVASCRIPT RULES
    // =============================================================================
    'no-console': 'warn',
    'no-debugger': 'error',
    'no-unused-vars': 'off', // Handled by @typescript-eslint/no-unused-vars
    'no-undef': 'error',
    'no-var': 'error',
    'prefer-const': 'error',
    'prefer-arrow-callback': 'error',
    'arrow-spacing': 'error',
    'no-duplicate-imports': 'error',
    'no-useless-return': 'error',
    'no-useless-constructor': 'error',
    'no-useless-rename': 'error',
    'object-shorthand': 'error',
    'prefer-template': 'error',
    'template-curly-spacing': 'error',

    // =============================================================================
    // IMPORT RULES
    // =============================================================================
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
        ],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],
    'import/no-unresolved': 'error',
    'import/no-cycle': 'error',
    'import/no-self-import': 'error',
    'import/no-useless-path-segments': 'error',

    // =============================================================================
    // SECURITY RULES
    // =============================================================================
    'security/detect-object-injection': 'warn',
    'security/detect-non-literal-regexp': 'warn',
    'security/detect-unsafe-regex': 'error',
    'security/detect-buffer-noassert': 'error',
    'security/detect-child-process': 'warn',
    'security/detect-disable-mustache-escape': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-no-csrf-before-method-override': 'error',
    'security/detect-non-literal-fs-filename': 'warn',
    'security/detect-non-literal-require': 'warn',
    'security/detect-possible-timing-attacks': 'warn',
    'security/detect-pseudoRandomBytes': 'error',

    // =============================================================================
    // JEST RULES
    // =============================================================================
    'jest/no-disabled-tests': 'warn',
    'jest/no-focused-tests': 'error',
    'jest/no-identical-title': 'error',
    'jest/prefer-to-have-length': 'warn',
    'jest/valid-expect': 'error',

    // =============================================================================
    // CODE QUALITY RULES
    // =============================================================================
    'complexity': ['warn', 10],
    'max-depth': ['warn', 4],
    'max-lines': ['warn', 300],
    'max-lines-per-function': ['warn', 50],
    'max-params': ['warn', 4],
    'no-magic-numbers': ['warn', { ignore: [0, 1, -1] }],
    'no-nested-ternary': 'error',
    'no-unneeded-ternary': 'error',
    'prefer-destructuring': 'error',
    'prefer-spread': 'error',
    'prefer-rest-params': 'error',

    // =============================================================================
    // STYLE RULES
    // =============================================================================
    'camelcase': 'error',
    'consistent-return': 'error',
    'default-case': 'error',
    'eqeqeq': 'error',
    'no-alert': 'error',
    'no-caller': 'error',
    'no-eval': 'error',
    'no-extend-native': 'error',
    'no-extra-bind': 'error',
    'no-implied-eval': 'error',
    'no-iterator': 'error',
    'no-labels': 'error',
    'no-lone-blocks': 'error',
    'no-loop-func': 'error',
    'no-multi-spaces': 'error',
    'no-multi-str': 'error',
    'no-new': 'error',
    'no-new-func': 'error',
    'no-new-wrappers': 'error',
    'no-octal-escape': 'error',
    'no-proto': 'error',
    'no-return-assign': 'error',
    'no-script-url': 'error',
    'no-self-compare': 'error',
    'no-sequences': 'error',
    'no-throw-literal': 'error',
    'no-unused-expressions': 'error',
    'no-useless-call': 'error',
    'no-useless-concat': 'error',
    'no-void': 'error',
    'no-with': 'error',
    'radix': 'error',
    'wrap-iife': 'error',
    'yoda': 'error',
  },

  // =============================================================================
  // OVERRIDE RULES FOR SPECIFIC FILE TYPES
  // =============================================================================
  overrides: [
    // =============================================================================
    // TEST FILES
    // =============================================================================
    {
      files: ['**/*.test.{js,ts,jsx,tsx}', '**/*.spec.{js,ts,jsx,tsx}'],
      env: {
        jest: true,
      },
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        'no-magic-numbers': 'off',
        'max-lines-per-function': 'off',
      },
    },

    // =============================================================================
    // CONFIG FILES
    // =============================================================================
    {
      files: ['*.config.{js,ts}', '*.config.*.{js,ts}'],
      env: {
        node: true,
      },
      rules: {
        '@typescript-eslint/no-var-requires': 'off',
        'no-console': 'off',
      },
    },

    // =============================================================================
    // MIGRATION FILES
    // =============================================================================
    {
      files: ['**/migrations/**/*.{js,ts}'],
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        'no-console': 'off',
      },
    },
  ],

  // =============================================================================
  // IGNORE PATTERNS
  // =============================================================================
  ignorePatterns: [
    'node_modules/',
    'dist/',
    'build/',
    'coverage/',
    '*.min.js',
    '*.bundle.js',
    '.next/',
    '.nuxt/',
    '.vuepress/dist/',
    '.serverless/',
    '.fusebox/',
    '.dynamodb/',
    '.tern-port/',
    'cypress/videos/',
    'cypress/screenshots/',
  ],

  // =============================================================================
  // SETTINGS
  // =============================================================================
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
      node: {
        extensions: ['.js', '.jsx', '.ts', '.tsx'],
      },
    },
  },
};
