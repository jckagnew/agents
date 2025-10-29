#!/usr/bin/env node
const { spawnSync } = require('child_process');
const { getClient } = require('./llm-clients');

const args = process.argv.slice(2);
const providerIndex = args.indexOf('--provider');
const taskIndex = args.indexOf('--task');
const sessionIndex = args.indexOf('--session-dir');
const fallbackIndex = args.indexOf('--fallback');

const provider = providerIndex >= 0 ? args[providerIndex + 1] : process.env.LLM_DEFAULT_PROVIDER;
const fallback = fallbackIndex >= 0 ? args[fallbackIndex + 1] : null;
const task = taskIndex >= 0 ? args[taskIndex + 1] : null;
const sessionDir = sessionIndex >= 0 ? args[sessionIndex + 1] : null;

if (!task) {
  console.error('Usage: node scripts/run-with-llm.js --task <command> [--session-dir <path>] [--provider <name>] [--fallback <name>]');
  process.exit(1);
}

(async () => {
  try {
    const client = getClient(provider);
    console.log(`Using provider: ${provider}`);
    const result = spawnSync('bash', ['-lc', task], { stdio: 'inherit', env: process.env });
    if (result.status !== 0 && fallback) {
      console.warn(`Task failed with provider ${provider}, trying fallback ${fallback}`);
      const fallbackClient = getClient(fallback);
      console.log(`Using fallback provider: ${fallback}`);
      const fallbackResult = spawnSync('bash', ['-lc', task], { stdio: 'inherit', env: process.env });
      process.exit(fallbackResult.status);
    } else {
      process.exit(result.status);
    }
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
})();
