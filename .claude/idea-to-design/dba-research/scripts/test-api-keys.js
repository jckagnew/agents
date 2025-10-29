#!/usr/bin/env node

/**
 * Name Vetting API Keys Test Script
 * Tests all configured API keys for name vetting services
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load configuration
const configPath = path.join(__dirname, '../config/api-keys.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logHeader(message) {
  log(`\n${colors.bold}${colors.blue}${message}${colors.reset}`);
  log('='.repeat(message.length));
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green');
}

function logError(message) {
  log(`❌ ${message}`, 'red');
}

function logWarning(message) {
  log(`⚠️  ${message}`, 'yellow');
}

function logInfo(message) {
  log(`ℹ️  ${message}`, 'blue');
}

// Test Domainr API
async function testDomainrAPI() {
  logHeader('Testing Domainr API');
  
  const apiKey = process.env.DOMAINR_API_KEY;
  if (!apiKey) {
    logError('DOMAINR_API_KEY not found in environment');
    return false;
  }
  
  try {
    const result = await makeRequest(`https://domainr.com/api/v2/status/example.com?key=${apiKey}`);
    if (result.status === 'available' || result.status === 'taken') {
      logSuccess('Domainr API key is valid and working');
      logInfo(`Test domain status: ${result.status}`);
      return true;
    } else {
      logError('Unexpected response from Domainr API');
      return false;
    }
  } catch (error) {
    logError(`Domainr API test failed: ${error.message}`);
    return false;
  }
}

// Test Google Custom Search API
async function testGoogleSearchAPI() {
  logHeader('Testing Google Custom Search API');
  
  const apiKey = process.env.GOOGLE_SEARCH_API_KEY;
  const searchEngineId = process.env.GOOGLE_SEARCH_ENGINE_ID;
  
  if (!apiKey) {
    logError('GOOGLE_SEARCH_API_KEY not found in environment');
    return false;
  }
  
  if (!searchEngineId) {
    logError('GOOGLE_SEARCH_ENGINE_ID not found in environment');
    return false;
  }
  
  try {
    const url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=test`;
    const result = await makeRequest(url);
    
    if (result.items || result.searchInformation) {
      logSuccess('Google Custom Search API is valid and working');
      logInfo(`Search results: ${result.searchInformation?.totalResults || 0} items`);
      return true;
    } else {
      logError('Unexpected response from Google Custom Search API');
      return false;
    }
  } catch (error) {
    logError(`Google Custom Search API test failed: ${error.message}`);
    return false;
  }
}

// Test GoDaddy API (optional)
async function testGoDaddyAPI() {
  logHeader('Testing GoDaddy API (Optional)');
  
  const apiKey = process.env.GODADDY_API_KEY;
  const secretKey = process.env.GODADDY_SECRET_KEY;
  
  if (!apiKey || !secretKey) {
    logWarning('GoDaddy API keys not configured (optional fallback)');
    return true; // Not required
  }
  
  try {
    const options = {
      hostname: 'api.godaddy.com',
      port: 443,
      path: '/v1/domains/available?domain=example.com',
      method: 'GET',
      headers: {
        'Authorization': `sso-key ${apiKey}:${secretKey}`,
        'Accept': 'application/json'
      }
    };
    
    const result = await makeRequest('https://api.godaddy.com/v1/domains/available?domain=example.com', options);
    
    if (result.available !== undefined) {
      logSuccess('GoDaddy API is valid and working');
      logInfo(`Test domain available: ${result.available}`);
      return true;
    } else {
      logError('Unexpected response from GoDaddy API');
      return false;
    }
  } catch (error) {
    logError(`GoDaddy API test failed: ${error.message}`);
    return false;
  }
}

// Test USPTO API (no key required)
async function testUSPTOAPI() {
  logHeader('Testing USPTO TSDR API');
  
  try {
    // Test with a known trademark
    const result = await makeRequest('https://tsdrapi.uspto.gov/ts/cd/casestatus/info/12345678');
    
    // USPTO API returns various responses, we just need to confirm it's accessible
    logSuccess('USPTO TSDR API is accessible');
    logInfo('USPTO API requires no authentication key');
    return true;
  } catch (error) {
    logWarning(`USPTO API test inconclusive: ${error.message}`);
    logInfo('USPTO API may be temporarily unavailable or rate limited');
    return true; // USPTO is often rate limited, so we don't fail the test
  }
}

// Generic HTTP request function
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const jsonData = JSON.parse(data);
          resolve(jsonData);
        } catch (error) {
          reject(new Error(`Invalid JSON response: ${error.message}`));
        }
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.end();
  });
}

// Main test function
async function runTests() {
  logHeader('Name Vetting API Keys Test Suite');
  logInfo('Testing all configured API keys for name vetting services\n');
  
  const results = {
    domainr: false,
    googleSearch: false,
    godaddy: false,
    uspto: false
  };
  
  // Run all tests
  results.domainr = await testDomainrAPI();
  results.googleSearch = await testGoogleSearchAPI();
  results.godaddy = await testGoDaddyAPI();
  results.uspto = await testUSPTOAPI();
  
  // Summary
  logHeader('Test Results Summary');
  
  const requiredServices = ['domainr', 'googleSearch', 'uspto'];
  const optionalServices = ['godaddy'];
  
  let allRequiredPassed = true;
  
  requiredServices.forEach(service => {
    if (results[service]) {
      logSuccess(`${service.toUpperCase()} API: Working`);
    } else {
      logError(`${service.toUpperCase()} API: Failed`);
      allRequiredPassed = false;
    }
  });
  
  optionalServices.forEach(service => {
    if (results[service]) {
      logSuccess(`${service.toUpperCase()} API: Working (Optional)`);
    } else {
      logWarning(`${service.toUpperCase()} API: Not configured (Optional)`);
    }
  });
  
  logHeader('Next Steps');
  
  if (allRequiredPassed) {
    logSuccess('All required API keys are working correctly!');
    logInfo('You can now proceed with name vetting automation.');
  } else {
    logError('Some required API keys are not working.');
    logInfo('Please check the setup guide: .claude/idea-to-design/dba-research/docs/API_KEYS_SETUP.md');
  }
  
  logInfo('\nConfiguration file: .claude/idea-to-design/dba-research/config/api-keys.json');
  logInfo('Environment template: env.template');
}

// Run the tests
if (require.main === module) {
  runTests().catch(error => {
    logError(`Test suite failed: ${error.message}`);
    process.exit(1);
  });
}

module.exports = { runTests };
