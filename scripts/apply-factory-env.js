#!/usr/bin/env node
/*
 * Synchronises Factory Supabase env variables into every project-level .env file.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const ROOT_ENV = path.join(ROOT, '.env');

const REQUIRED_KEYS = [
  'FACTORY_SUPABASE_URL',
  'FACTORY_SUPABASE_SERVICE_KEY',
  'FACTORY_SUPABASE_ANON_KEY',
  'EXPO_PUBLIC_FACTORY_SUPABASE_URL',
  'EXPO_PUBLIC_FACTORY_SUPABASE_SERVICE_KEY',
  'EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY',
];

function parseEnvFile(filePath) {
  const vars = {};
  if (!fs.existsSync(filePath)) {
    return vars;
  }
  const lines = fs.readFileSync(filePath, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    if (!line || line.trim().startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    const value = line.slice(idx + 1).trim();
    if (key) vars[key] = value;
  }
  return vars;
}

function ensureEnvVars(filePath, sourceVars) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, '', 'utf8');
  }
  const current = parseEnvFile(filePath);
  const additions = [];
  for (const key of REQUIRED_KEYS) {
    const value = sourceVars[key];
    if (!value) continue; // skip missing values
    if (!(key in current)) {
      additions.push(`${key}=${value}`);
    }
  }
  if (additions.length > 0) {
    fs.appendFileSync(filePath, `\n# Factory observability\n${additions.join('\n')}\n`, 'utf8');
    console.log(`[factory-env] Added keys to ${path.relative(ROOT, filePath)}`);
  }
}

function collectEnvFiles(startDir) {
  const results = [];
  const stack = [startDir];
  const ignore = new Set(['node_modules', '.git', '.test-dist', '.expo']);
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (ignore.has(entry.name)) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        stack.push(full);
      } else if (entry.isFile() && entry.name === '.env' && full !== ROOT_ENV) {
        results.push(full);
      }
    }
  }
  return results;
}

if (!fs.existsSync(ROOT_ENV)) {
  console.error('[factory-env] Root .env not found. Aborting.');
  process.exit(1);
}

const rootVars = parseEnvFile(ROOT_ENV);
const missing = REQUIRED_KEYS.filter(k => !rootVars[k]);
if (missing.length) {
  console.warn('[factory-env] Warning: missing values in root .env:', missing.join(', '));
}

const envFiles = collectEnvFiles(ROOT);
for (const envPath of envFiles) {
  ensureEnvVars(envPath, rootVars);
}

console.log(`[factory-env] Processed ${envFiles.length} .env files.`);
