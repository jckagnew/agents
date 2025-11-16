#!/usr/bin/env node

// Load environment variables
require('dotenv').config();

/**
 * Name Vetting Automation
 *
 * Validates business names through domain availability, trademark screening,
 * and social handle availability checks. Produces a scored report to help
 * select the best name candidate.
 *
 * Usage:
 *   node scripts/name-vetting.js --names "Acme Corp,Widget Labs,Tech Solutions"
 *   node scripts/name-vetting.js --input names.json --output vetting-report.json
 *   node scripts/name-vetting.js --name "Acme Corp" --deep-check
 *
 * Scoring Logic:
 *   - Domain Availability (0-40 points): .com available = 40, .io/.co = 30, other = 20
 *   - Trademark Risk (0-30 points): No conflicts = 30, Similar marks = 15, Direct conflict = 0
 *   - Social Handle Availability (0-20 points): All available = 20, 2/3 = 13, 1/3 = 7
 *   - Uniqueness (0-30 points): 0 results = 30, 1-100 = 25, 101-1000 = 15, 1001-10000 = 8, >10000 = 0
 *
 *   Total Score: 0-120 (84+ = Excellent, 60-83 = Good, 36-59 = Risky, <36 = Avoid)
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
  // API endpoints (TODO: Add actual API keys to env variables)
  apis: {
    domainr: {
      endpoint: 'https://api.domainr.com/v2',
      apiKey: process.env.DOMAINR_API_KEY || null,
    },
    godaddy: {
      endpoint: 'https://api.godaddy.com/v1',
      apiKey: process.env.GODADDY_API_KEY || null,
      secret: process.env.GODADDY_API_SECRET || null,
    },
    uspto: {
      endpoint: 'https://developer.uspto.gov/api/v1',
      apiKey: process.env.USPTO_API_KEY || null,
    },
    patentsView: {
      endpoint: 'https://api.patentsview.org/patents/query',
    },
    gemini: {
      endpoint: 'https://generativelanguage.googleapis.com/v1beta/models',
      apiKey: process.env.GEMINI_API_KEY || null,
      model: (process.env.GEMINI_MODEL || 'gemini-1.5-flash-latest').trim(),
    },
    ollama: {
      endpoint: (process.env.OLLAMA_ENDPOINT || 'http://127.0.0.1:11434').replace(/\/$/, ''),
      model: (process.env.OLLAMA_MODEL || 'llama3').trim(),
      provider: (process.env.UNIQUE_CHECK_PROVIDER || '').trim().toLowerCase(),
    },
  },

  // Scoring weights
  scoring: {
    domainAvailability: 40,
    trademarkRisk: 30,
    socialAvailability: 20,
    uniqueness: 30,
  },

  // Domain extensions to check (in priority order)
  domainExtensions: ['.com', '.io', '.co', '.app', '.tech', '.ai'],

  // Social platforms to check
  socialPlatforms: ['twitter', 'instagram', 'linkedin'],

  // Thresholds
  thresholds: {
    excellent: 70,
    good: 50,
    risky: 30,
  },
};

// ============================================================================
// Domain Availability Checks
// ============================================================================

/**
 * TODO: Implement domain availability check using Domainr or GoDaddy API
 *
 * Steps:
 * 1. Convert business name to valid domain format (lowercase, remove spaces/special chars)
 * 2. For each domain extension in CONFIG.domainExtensions:
 *    a. Call Domainr API /v2/status endpoint with domain query
 *    b. Parse response to determine availability (available, taken, unavailable)
 *    c. Store result with extension priority
 * 3. If Domainr unavailable, fall back to GoDaddy API /v1/domains/available
 * 4. Return availability results with scoring:
 *    - .com available = 40 points
 *    - .io or .co available = 30 points
 *    - Other TLDs available = 20 points
 *    - No domains available = 0 points
 *
 * @param {string} businessName - The business name to check
 * @returns {Promise<Object>} Domain availability results
 *   {
 *     available: [{extension: '.com', domain: 'acmecorp.com', available: true}],
 *     unavailable: [{extension: '.com', domain: 'acmecorp.com', available: false}],
 *     score: 40,
 *     bestDomain: 'acmecorp.com',
 *     notes: 'Premium .com domain available'
 *   }
 */
async function checkDomainAvailability(businessName) {
  console.log(`🌐 Checking domain availability for: ${businessName}`);

  const normalizedName = normalizeToDomain(businessName);
  const available = [];
  const unavailable = [];
  const details = [];

  // Build list of domains to check
  const domainsToCheck = CONFIG.domainExtensions.map(ext => normalizedName + ext);

  try {
    // Try Domainr API first
    if (CONFIG.apis.domainr.apiKey) {
      console.log('   Using Domainr API...');
      const results = await checkDomainrAvailability(domainsToCheck);

      for (const result of results) {
        const ext = result.domain.replace(normalizedName, '');
        const domainInfo = {
          extension: ext,
          domain: result.domain,
          available: result.availability === 'available',
          availability: result.availability,
          priceHint: result.priceHint,
        };

        if (result.availability === 'available') {
          available.push(domainInfo);
        } else {
          unavailable.push(domainInfo);
        }
        details.push(domainInfo);
      }
    } else {
      console.log('   ⚠️  Domainr API key not found, trying GoDaddy...');

      // Fall back to GoDaddy
      if (CONFIG.apis.godaddy.apiKey && CONFIG.apis.godaddy.secret) {
        const results = await checkGoDaddyAvailability(domainsToCheck);

        for (const result of results) {
          const ext = result.domain.replace(normalizedName, '');
          const domainInfo = {
            extension: ext,
            domain: result.domain,
            available: result.availability === 'available',
            availability: result.availability,
            priceHint: result.priceHint,
          };

          if (result.availability === 'available') {
            available.push(domainInfo);
          } else {
            unavailable.push(domainInfo);
          }
          details.push(domainInfo);
        }
      } else {
        console.log('   ⚠️  GoDaddy API credentials not found');
        // Return unknown status for all domains
        for (const domain of domainsToCheck) {
          const ext = domain.replace(normalizedName, '');
          const domainInfo = {
            extension: ext,
            domain: domain,
            available: false,
            availability: 'unknown',
            priceHint: null,
          };
          unavailable.push(domainInfo);
          details.push(domainInfo);
        }
      }
    }
  } catch (error) {
    console.error(`   ❌ Error checking domain availability: ${error.message}`);

    // Return unknown status for all domains on error
    for (const domain of domainsToCheck) {
      const ext = domain.replace(normalizedName, '');
      const domainInfo = {
        extension: ext,
        domain: domain,
        available: false,
        availability: 'unknown',
        priceHint: null,
      };
      unavailable.push(domainInfo);
      details.push(domainInfo);
    }
  }

  // Calculate score based on available domains
  let score = 0;
  let bestDomain = null;
  let notes = '';

  if (available.length > 0) {
    // Prioritize by extension
    const comDomain = available.find(d => d.extension === '.com');
    const ioDomain = available.find(d => d.extension === '.io');
    const coDomain = available.find(d => d.extension === '.co');

    if (comDomain) {
      score = 40;
      bestDomain = comDomain.domain;
      notes = comDomain.availability === 'premium'
        ? `Premium .com domain available${comDomain.priceHint ? ` (${comDomain.priceHint})` : ''}`
        : 'Premium .com domain available';
    } else if (ioDomain || coDomain) {
      score = 30;
      bestDomain = (ioDomain || coDomain).domain;
      const domain = ioDomain || coDomain;
      notes = `${domain.extension} domain available${domain.availability === 'premium' ? ' (premium)' : ''}`;
    } else {
      score = 20;
      bestDomain = available[0].domain;
      notes = `${available[0].extension} domain available${available[0].availability === 'premium' ? ' (premium)' : ''}`;
    }
  } else if (details.some(d => d.availability === 'unknown')) {
    notes = 'Unable to verify domain availability - API keys not configured';
  } else {
    notes = 'No domains available - consider alternative names';
  }

  console.log(`   ✓ Found ${available.length} available domains`);
  if (bestDomain) {
    console.log(`   ✓ Best domain: ${bestDomain} (${score} points)`);
  }

  return {
    available,
    unavailable,
    details,
    score,
    bestDomain,
    notes,
  };
}

/**
 * Check domain availability using Domainr API
 *
 * @param {string[]} domains - Array of domains to check
 * @returns {Promise<Array>} Array of domain availability results
 */
async function checkDomainrAvailability(domains) {
  const results = [];

  // Domainr allows multiple domains in one request
  const domainParams = domains.map(d => `domain=${encodeURIComponent(d)}`).join('&');
  const url = `${CONFIG.apis.domainr.endpoint}/status?${domainParams}&client_id=${CONFIG.apis.domainr.apiKey}`;

  try {
    const https = require('https');
    const response = await new Promise((resolve, reject) => {
      https.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve(JSON.parse(data));
          } else {
            reject(new Error(`Domainr API returned status ${res.statusCode}: ${data}`));
          }
        });
      }).on('error', reject);
    });

    // Parse Domainr response
    // Response format: { status: [{ domain: 'example.com', summary: 'inactive|active|undelegated', status: '...', zone: '...' }] }
    for (const statusObj of (response.status || [])) {
      const availability = parseDomainrStatus(statusObj);
      results.push({
        domain: statusObj.domain,
        availability: availability.status,
        priceHint: availability.priceHint,
        rawStatus: statusObj,
      });
    }
  } catch (error) {
    console.error(`   ⚠️  Domainr API error: ${error.message}`);
    throw error;
  }

  return results;
}

/**
 * Parse Domainr status response to determine availability
 *
 * @param {Object} statusObj - Domainr status object
 * @returns {Object} Parsed availability
 */
function parseDomainrStatus(statusObj) {
  const summary = (statusObj.summary || '').toLowerCase();

  // Domainr summary values:
  // - 'inactive' or 'undelegated' = likely available
  // - 'active' = taken
  // - 'premium' = available but premium pricing
  // - 'parked' = taken/parked

  if (summary.includes('inactive') || summary.includes('undelegated')) {
    return { status: 'available', priceHint: null };
  } else if (summary.includes('premium')) {
    return { status: 'premium', priceHint: 'Premium pricing' };
  } else if (summary.includes('active') || summary.includes('parked')) {
    return { status: 'taken', priceHint: null };
  } else {
    return { status: 'unknown', priceHint: null };
  }
}

/**
 * Check domain availability using GoDaddy API
 *
 * @param {string[]} domains - Array of domains to check
 * @returns {Promise<Array>} Array of domain availability results
 */
async function checkGoDaddyAvailability(domains) {
  const results = [];
  const https = require('https');

  // GoDaddy requires checking domains one at a time
  for (const domain of domains) {
    const url = `${CONFIG.apis.godaddy.endpoint}/domains/available?domain=${encodeURIComponent(domain)}`;

    try {
      const response = await new Promise((resolve, reject) => {
        const options = {
          headers: {
            'Authorization': `sso-key ${CONFIG.apis.godaddy.apiKey}:${CONFIG.apis.godaddy.secret}`,
            'Accept': 'application/json',
          }
        };

        https.get(url, options, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            if (res.statusCode === 200) {
              resolve(JSON.parse(data));
            } else {
              reject(new Error(`GoDaddy API returned status ${res.statusCode}: ${data}`));
            }
          });
        }).on('error', reject);
      });

      // Parse GoDaddy response
      // Response format: { available: true|false, domain: 'example.com', price: 12990000 (in micro-units) }
      const availability = response.available ? 'available' : 'taken';
      const priceHint = response.price ? `$${(response.price / 1000000).toFixed(2)}` : null;

      results.push({
        domain: domain,
        availability: availability,
        priceHint: priceHint,
        rawResponse: response,
      });
    } catch (error) {
      console.error(`   ⚠️  GoDaddy API error for ${domain}: ${error.message}`);
      // On error, mark as unknown
      results.push({
        domain: domain,
        availability: 'unknown',
        priceHint: null,
      });
    }
  }

  return results;
}

/**
 * Helper function to normalize business name to domain format
 *
 * @param {string} name - Business name
 * @returns {string} Domain-safe name (lowercase, no spaces, alphanumeric only)
 */
function normalizeToDomain(name) {
  return name
    .toLowerCase()
    .trim()
    // Replace common word separators with empty string
    .replace(/[\s\-_\.]+/g, '')
    // Remove special characters, keep only alphanumeric
    .replace(/[^a-z0-9]/g, '')
    // Handle edge case: if name starts with number, domains don't allow that
    // But for now we'll allow it and let the API handle it
    ;
}

// ============================================================================
// Trademark Screening
// ============================================================================

/**
 * TODO: Implement trademark lookup via USPTO API and PatentsView
 *
 * Steps:
 * 1. Normalize business name for trademark search
 * 2. Query USPTO Trademark Status & Document Retrieval (TSDR) API:
 *    a. Endpoint: https://developer.uspto.gov/api/v1/trademark
 *    b. Search for exact and similar marks (use fuzzy matching)
 *    c. Filter by status: Active, Pending, Abandoned
 *    d. Parse results to identify conflicts
 * 3. Alternative: Use PatentsView API for broader search
 * 4. Analyze results:
 *    - Direct exact match (active) = HIGH RISK (0 points)
 *    - Similar marks in same industry = MEDIUM RISK (15 points)
 *    - No conflicts = LOW RISK (30 points)
 * 5. Return risk assessment with details
 *
 * @param {string} businessName - The business name to check
 * @param {string} industry - Business industry/category (optional)
 * @returns {Promise<Object>} Trademark risk assessment
 *   {
 *     conflicts: [{
 *       mark: 'ACME CORP',
 *       serialNumber: '88888888',
 *       status: 'Active',
 *       owner: 'Acme Industries Inc.',
 *       class: '009',
 *       similarity: 0.95
 *     }],
 *     riskLevel: 'high' | 'medium' | 'low',
 *     score: 0-30,
 *     notes: 'Direct trademark conflict found',
 *     recommendation: 'Avoid this name or consult trademark attorney'
 *   }
 */
async function checkTrademarkConflicts(businessName, industry = null) {
  console.log(`™️  Checking trademark conflicts for: ${businessName}`);

  // Normalize name for trademark search
  const normalizedName = normalizeToTrademark(businessName);
  const similarMarks = [];
  let conflictRisk = 'NONE';
  let apiUsed = 'none';

  try {
    // Try USPTO API first
    if (CONFIG.apis.uspto.apiKey) {
      console.log('   Using USPTO Trademark API...');
      const results = await searchUSPTOTrademarks(normalizedName);
      apiUsed = 'USPTO';

      // Analyze results for conflicts
      for (const mark of results) {
        const similarity = calculateTrademarkSimilarity(normalizedName, mark.markName);

        // Only include marks with similarity >= 0.4
        if (similarity >= 0.4) {
          similarMarks.push({
            name: mark.markName,
            owner: mark.owner,
            status: mark.status,
            class: mark.niceClasses,
            similarity: similarity,
            serialNumber: mark.serialNumber,
            filingDate: mark.filingDate,
          });
        }
      }
    } else {
      console.log('   ⚠️  USPTO API key not found, trying fallback...');

      // Try fallback APIs
      // Note: PatentsView doesn't have trademark data, so we'll return unknown
      console.log('   ⚠️  No fallback API available for trademark screening');
      apiUsed = 'none';
    }
  } catch (error) {
    console.error(`   ⚠️  Trademark screening error: ${error.message}`);
    apiUsed = 'error';
  }

  // Calculate conflict risk based on similarity scores
  if (apiUsed === 'none' || apiUsed === 'error') {
    conflictRisk = 'UNKNOWN';
  } else if (similarMarks.length === 0) {
    conflictRisk = 'NONE';
  } else {
    // Find highest similarity among LIVE marks (prioritize active registrations)
    const liveMarks = similarMarks.filter(m => m.status === 'LIVE');
    const highestSimilarity = Math.max(
      ...similarMarks.map(m => m.similarity),
      0
    );
    const highestLiveSimilarity = liveMarks.length > 0
      ? Math.max(...liveMarks.map(m => m.similarity))
      : 0;

    // Risk assessment based on similarity and status
    if (highestSimilarity >= 0.85 || highestLiveSimilarity >= 0.85) {
      conflictRisk = 'HIGH';
    } else if (highestSimilarity >= 0.7 || highestLiveSimilarity >= 0.7) {
      conflictRisk = 'MEDIUM';
    } else {
      conflictRisk = 'LOW';
    }
  }

  // Calculate score (0-30 points)
  let score = 0;
  let notes = '';
  let recommendation = '';

  if (conflictRisk === 'UNKNOWN') {
    score = 0;
    notes = 'Unable to verify trademark status - API not configured';
    recommendation = 'Configure USPTO API key or consult trademark attorney';
  } else if (conflictRisk === 'NONE') {
    score = 30;
    notes = 'No trademark conflicts detected';
    recommendation = 'Proceed with trademark registration';
  } else if (conflictRisk === 'LOW') {
    score = 20;
    notes = `${similarMarks.length} similar trademark(s) found with low similarity`;
    recommendation = 'Minor similarity - consider trademark attorney review';
  } else if (conflictRisk === 'MEDIUM') {
    score = 10;
    const liveCount = similarMarks.filter(m => m.status === 'LIVE').length;
    notes = `${liveCount} active trademark(s) with moderate similarity`;
    recommendation = 'Moderate risk - consult trademark attorney before proceeding';
  } else {
    // HIGH risk
    score = 0;
    const liveCount = similarMarks.filter(m => m.status === 'LIVE').length;
    notes = `${liveCount} active trademark(s) with high similarity`;
    recommendation = '⚠️  High conflict risk - strongly recommend selecting alternative name';
  }

  console.log(`   ✓ Risk: ${conflictRisk} (${similarMarks.length} similar marks found)`);
  console.log(`   ✓ Score: ${score}/30 points`);

  return {
    conflicts: similarMarks,
    conflictRisk,
    riskLevel: conflictRisk.toLowerCase(), // For backward compatibility
    score,
    notes,
    recommendation,
    apiUsed,
  };
}

/**
 * Search USPTO trademark database
 *
 * @param {string} markName - Normalized trademark name to search
 * @returns {Promise<Array>} Array of trademark results
 */
async function searchUSPTOTrademarks(markName) {
  const https = require('https');
  const results = [];

  // USPTO IBD API endpoint for trademark publications
  // Note: The actual USPTO API structure may vary - this is based on the specification
  const searchQuery = encodeURIComponent(`mark_identification:("${markName}")`);
  const url = `https://developer.uspto.gov/ibd-api/v1/trademark/application/publications?searchText=${searchQuery}&start=0&rows=10`;

  try {
    const response = await new Promise((resolve, reject) => {
      const options = {
        headers: {
          'Accept': 'application/json',
        }
      };

      // Add API key if available (may be in header or query param depending on USPTO requirements)
      if (CONFIG.apis.uspto.apiKey) {
        options.headers['Authorization'] = `Bearer ${CONFIG.apis.uspto.apiKey}`;
      }

      const req = https.get(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve(JSON.parse(data));
          } else if (res.statusCode === 429) {
            // Rate limit - retry after delay
            setTimeout(() => {
              searchUSPTOTrademarks(markName).then(resolve).catch(reject);
            }, 2000);
          } else {
            reject(new Error(`USPTO API returned status ${res.statusCode}: ${data}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(10000, () => {
        req.destroy();
        reject(new Error('USPTO API request timeout'));
      });
    });

    // Parse USPTO response
    // Response structure varies by API version - adapt as needed
    const docs = response.response?.docs || response.docs || [];

    for (const doc of docs) {
      // Extract relevant fields from USPTO response
      const markName = doc.markIdentification || doc.mark_identification || '';
      const owner = doc.applicantName || doc.applicant_name || doc.ownerName || 'Unknown';
      const status = parseUSPTOStatus(doc.markCurrentStatusType || doc.status || '');
      const serialNumber = doc.serialNumber || doc.serial_number || '';
      const filingDate = doc.filingDate || doc.filing_date || '';

      // Parse Nice classification codes
      const niceClasses = parseNiceClasses(doc);

      results.push({
        markName,
        owner,
        status,
        niceClasses,
        serialNumber,
        filingDate,
        rawData: doc,
      });
    }
  } catch (error) {
    console.error(`   ⚠️  USPTO API error: ${error.message}`);
    throw error;
  }

  return results;
}

/**
 * Parse USPTO status to LIVE/DEAD
 *
 * @param {string} status - Raw USPTO status
 * @returns {string} Simplified status (LIVE or DEAD)
 */
function parseUSPTOStatus(status) {
  const statusLower = String(status).toLowerCase();

  // Active/live statuses
  if (statusLower.includes('registered') ||
      statusLower.includes('published') ||
      statusLower.includes('approved') ||
      statusLower.includes('active') ||
      statusLower.includes('live')) {
    return 'LIVE';
  }

  // Dead/abandoned statuses
  if (statusLower.includes('abandoned') ||
      statusLower.includes('cancelled') ||
      statusLower.includes('expired') ||
      statusLower.includes('dead')) {
    return 'DEAD';
  }

  // Pending statuses - treat as LIVE for safety
  if (statusLower.includes('pending') ||
      statusLower.includes('filed') ||
      statusLower.includes('opposition')) {
    return 'LIVE';
  }

  // Default to LIVE to be conservative
  return 'LIVE';
}

/**
 * Parse Nice classification codes from USPTO response
 *
 * @param {Object} doc - USPTO document
 * @returns {string} Comma-separated Nice classes
 */
function parseNiceClasses(doc) {
  // Try various field names that might contain Nice classes
  const classFields = [
    doc.internationalClassCodes,
    doc.international_class_codes,
    doc.niceClasses,
    doc.nice_classes,
    doc.classList,
    doc.class_list,
  ];

  for (const field of classFields) {
    if (field) {
      if (Array.isArray(field)) {
        return field.join(', ');
      }
      return String(field);
    }
  }

  return '';
}

/**
 * Normalize business name for trademark search
 *
 * @param {string} name - Business name
 * @returns {string} Normalized name (uppercase, alphanumeric only)
 */
function normalizeToTrademark(name) {
  return name
    .toUpperCase()
    .trim()
    // Remove common legal suffixes
    .replace(/\b(INC|LLC|LTD|CORP|CO|CORPORATION|LIMITED|COMPANY)\b/g, '')
    .trim()
    // Keep only alphanumeric and spaces
    .replace(/[^A-Z0-9\s]/g, '')
    // Normalize multiple spaces to single space
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Calculate trademark similarity score using Levenshtein distance
 *
 * @param {string} name1 - First name (normalized)
 * @param {string} name2 - Second name (will be normalized)
 * @returns {number} Similarity score (0.0 = different, 1.0 = identical)
 */
function calculateTrademarkSimilarity(name1, name2) {
  // Normalize both names for comparison
  const norm1 = normalizeToTrademark(name1);
  const norm2 = normalizeToTrademark(name2);

  // Handle edge cases
  if (norm1 === norm2) return 1.0;
  if (norm1.length === 0 || norm2.length === 0) return 0.0;

  // Calculate Levenshtein distance
  const distance = levenshteinDistance(norm1, norm2);

  // Convert distance to similarity score (0.0 to 1.0)
  const maxLength = Math.max(norm1.length, norm2.length);
  const similarity = 1.0 - (distance / maxLength);

  return Math.max(0.0, Math.min(1.0, similarity));
}

/**
 * Calculate Levenshtein distance between two strings
 *
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {number} Edit distance
 */
function levenshteinDistance(str1, str2) {
  const len1 = str1.length;
  const len2 = str2.length;

  // Create distance matrix
  const matrix = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(0));

  // Initialize first column and row
  for (let i = 0; i <= len1; i++) {
    matrix[i][0] = i;
  }
  for (let j = 0; j <= len2; j++) {
    matrix[0][j] = j;
  }

  // Fill in the rest of the matrix
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,      // deletion
        matrix[i][j - 1] + 1,      // insertion
        matrix[i - 1][j - 1] + cost // substitution
      );
    }
  }

  return matrix[len1][len2];
}

// ============================================================================
// Social Handle Availability
// ============================================================================

/**
 * TODO: Implement social handle availability check
 *
 * Steps:
 * 1. Normalize business name to valid social handle (remove spaces, special chars)
 * 2. For each platform in CONFIG.socialPlatforms:
 *
 *    TWITTER/X:
 *    a. Try direct profile fetch: https://twitter.com/{handle}
 *    b. Check HTTP response: 404 = available, 200 = taken
 *    c. Alternative: Use Twitter API v2 GET /2/users/by/username/:username
 *
 *    INSTAGRAM:
 *    a. Try profile URL: https://www.instagram.com/{handle}/
 *    b. Parse response or use unofficial Instagram API
 *    c. Note: Instagram requires authentication for API access
 *
 *    LINKEDIN:
 *    a. Check company page: https://www.linkedin.com/company/{handle}
 *    b. LinkedIn API requires OAuth - consider web scraping as fallback
 *    c. Use LinkedIn Pages API if credentials available
 *
 * 3. Score results:
 *    - All 3 platforms available = 20 points
 *    - 2 of 3 available = 13 points
 *    - 1 of 3 available = 7 points
 *    - None available = 0 points
 *
 * 4. Return availability results with recommendations
 *
 * @param {string} businessName - The business name to check
 * @returns {Promise<Object>} Social handle availability
 *   {
 *     handles: {
 *       twitter: {handle: '@acmecorp', available: true, url: 'https://twitter.com/acmecorp'},
 *       instagram: {handle: '@acmecorp', available: false, url: 'https://instagram.com/acmecorp'},
 *       linkedin: {handle: 'acmecorp', available: true, url: 'https://linkedin.com/company/acmecorp'}
 *     },
 *     availableCount: 2,
 *     score: 13,
 *     notes: 'Twitter and LinkedIn available, Instagram taken',
 *     alternatives: ['acmecorp_', 'acmecorpofficial', 'theacmecorp']
 *   }
 */
async function checkSocialHandles(businessName) {
  console.log(`📱 Checking social handle availability for: ${businessName}`);

  try {
    // Generate handle variations
    const handleVariations = generateHandleVariations(businessName);
    const primaryHandle = handleVariations[0];

    // Check availability on each platform
    const platformAvailability = {
      twitter: await checkTwitterAvailability(primaryHandle),
      linkedin: await checkLinkedInAvailability(primaryHandle),
      instagram: await checkInstagramAvailability(primaryHandle)
    };

    // Calculate score based on availability
    const availableCount = Object.values(platformAvailability).filter(status => status === 'available').length;
    const score = calculateSocialScore(availableCount);

    // Generate suggestions for unavailable handles
    const suggestions = generateHandleSuggestions(businessName, platformAvailability);

  return {
      handle: primaryHandle,
      platformAvailability,
      availableCount,
      score,
      suggestions,
      notes: generateSocialNotes(platformAvailability, availableCount),
      handles: {
        twitter: {
          handle: `@${primaryHandle}`,
          available: platformAvailability.twitter === 'available',
          url: `https://twitter.com/${primaryHandle}`,
          status: platformAvailability.twitter
        },
        linkedin: {
          handle: primaryHandle,
          available: platformAvailability.linkedin === 'available',
          url: `https://www.linkedin.com/company/${primaryHandle}`,
          status: platformAvailability.linkedin
        },
        instagram: {
          handle: `@${primaryHandle}`,
          available: platformAvailability.instagram === 'available',
          url: `https://www.instagram.com/${primaryHandle}/`,
          status: platformAvailability.instagram
        }
      }
    };

  } catch (error) {
    console.error(`❌ Error checking social handles for ${businessName}:`, error.message);
    return {
      handle: normalizeToHandle(businessName),
      platformAvailability: {
        twitter: 'unknown',
        linkedin: 'unknown',
        instagram: 'unknown'
      },
      availableCount: 0,
      score: 0,
      suggestions: [],
      notes: `Error: ${error.message}`,
      handles: {}
    };
  }
}

/**
 * Generate handle variations for a business name
 */
function generateHandleVariations(businessName) {
  const normalized = normalizeToHandle(businessName);
  const variations = [normalized];

  // Add common variations
  if (normalized.length > 10) {
    variations.push(normalized.substring(0, 10));
  }

  // Add suffix variations
  variations.push(`${normalized}app`);
  variations.push(`${normalized}co`);
  variations.push(`${normalized}official`);

  // Add prefix variations
  variations.push(`hello${normalized}`);
  variations.push(`get${normalized}`);

  // Remove duplicates and return
  return [...new Set(variations)];
}

/**
 * Check Twitter/X handle availability
 */
async function checkTwitterAvailability(handle) {
  try {
    const url = `https://twitter.com/${handle}`;
    const response = await makeHttpRequest(url, {}, { method: 'HEAD', returnBody: true });
    
    if (response.status === 200) {
      // Check if it's a real profile or "This account doesn't exist" page
      const getResponse = await makeHttpRequest(url, {}, { method: 'GET', returnBody: true });
      const content = getResponse.body || '';
      
      if (content.includes('This account doesn\'t exist') || 
          content.includes('Account suspended') ||
          content.includes('Something went wrong')) {
        return 'available';
      }
      return 'taken';
    } else if (response.status === 404) {
      return 'available';
    } else {
      return 'unknown';
    }
  } catch (error) {
    console.log(`⚠️  Twitter check failed for ${handle}: ${error.message}`);
    return 'unknown';
  }
}

/**
 * Check LinkedIn company page availability
 */
async function checkLinkedInAvailability(handle) {
  try {
    const url = `https://www.linkedin.com/company/${handle}`;
    
    // Try HEAD request first
    try {
      const headResponse = await makeHttpRequest(url, {}, { method: 'HEAD', returnBody: true });
      if (headResponse.status === 200) {
        return 'taken';
      } else if (headResponse.status === 404) {
        return 'available';
      }
    } catch (headError) {
      // LinkedIn might block HEAD requests, fall back to GET
    }

    // Fall back to GET request
    const getResponse = await makeHttpRequest(url, {}, { method: 'GET', returnBody: true });
    
    if (getResponse.status === 200) {
      const content = getResponse.body || '';
      
      // Look for "Page Not Found" or similar indicators
      if (content.includes('Page Not Found') || 
          content.includes('This page doesn\'t exist') ||
          content.includes('Company not found')) {
        return 'available';
      }
      return 'taken';
    } else if (getResponse.status === 404) {
      return 'available';
    } else {
      return 'unknown';
    }
  } catch (error) {
    console.log(`⚠️  LinkedIn check failed for ${handle}: ${error.message}`);
    return 'unknown';
  }
}

/**
 * Check Instagram handle availability
 */
async function checkInstagramAvailability(handle) {
  try {
    const url = `https://www.instagram.com/${handle}/`;
    const response = await makeHttpRequest(url, {}, { method: 'HEAD', returnBody: true });
    
    if (response.status === 200) {
      // Instagram returns 200 even for non-existent profiles
      // We need to check the content to determine if it's real
      const getResponse = await makeHttpRequest(url, {}, { method: 'GET', returnBody: true });
      const content = getResponse.body || '';
      
      if (content.includes('Sorry, this page isn\'t available') ||
          content.includes('The link you followed may be broken') ||
          content.includes('User not found')) {
        return 'available';
      }
      return 'taken';
    } else if (response.status === 404) {
      return 'available';
    } else {
      return 'unknown';
    }
  } catch (error) {
    console.log(`⚠️  Instagram check failed for ${handle}: ${error.message}`);
    return 'unknown';
  }
}

/**
 * Calculate social handle score based on availability
 */
function calculateSocialScore(availableCount) {
  switch (availableCount) {
    case 3: return 20; // All platforms available
    case 2: return 13; // 2 of 3 available
    case 1: return 7;  // 1 of 3 available
    default: return 0; // None available
  }
}

/**
 * Generate handle suggestions for unavailable platforms
 */
function generateHandleSuggestions(businessName, platformAvailability) {
  const suggestions = [];
  const baseHandle = normalizeToHandle(businessName);

  // Only suggest if some platforms are unavailable
  const unavailablePlatforms = Object.entries(platformAvailability)
    .filter(([_, status]) => status === 'taken')
    .map(([platform, _]) => platform);

  if (unavailablePlatforms.length === 0) {
    return suggestions;
  }

  // Generate suggestions
  suggestions.push(`${baseHandle}_`);
  suggestions.push(`${baseHandle}app`);
  suggestions.push(`hello${baseHandle}`);
  suggestions.push(`get${baseHandle}`);
  suggestions.push(`${baseHandle}official`);
  suggestions.push(`${baseHandle}co`);
  suggestions.push(`the${baseHandle}`);

  // Add platform-specific suggestions
  if (unavailablePlatforms.includes('twitter')) {
    suggestions.push(`${baseHandle}inc`);
    suggestions.push(`${baseHandle}labs`);
  }

  return suggestions.slice(0, 5); // Limit to 5 suggestions
}

/**
 * Generate notes about social handle availability
 */
function generateSocialNotes(platformAvailability, availableCount) {
  const availablePlatforms = Object.entries(platformAvailability)
    .filter(([_, status]) => status === 'available')
    .map(([platform, _]) => platform);

  const takenPlatforms = Object.entries(platformAvailability)
    .filter(([_, status]) => status === 'taken')
    .map(([platform, _]) => platform);

  const unknownPlatforms = Object.entries(platformAvailability)
    .filter(([_, status]) => status === 'unknown')
    .map(([platform, _]) => platform);

  let notes = [];

  if (availablePlatforms.length > 0) {
    notes.push(`${availablePlatforms.join(', ')} available`);
  }

  if (takenPlatforms.length > 0) {
    notes.push(`${takenPlatforms.join(', ')} taken`);
  }

  if (unknownPlatforms.length > 0) {
    notes.push(`${unknownPlatforms.join(', ')} status unknown`);
  }

  return notes.join(', ');
}

/**
 * TODO: Helper to normalize name to social handle format
 *
 * @param {string} name - Business name
 * @param {string} platform - Platform name (for platform-specific rules)
 * @returns {string} Valid social handle
 */
function normalizeToHandle(name, platform) {
  // TODO: Implement normalization with platform-specific rules
  // Twitter: 15 chars max, alphanumeric + underscore
  // Instagram: 30 chars max, alphanumeric + period + underscore
  // LinkedIn: No strict limit, but recommend < 25 chars
  return name.toLowerCase().replace(/[^a-z0-9_]/g, '');
}

// ============================================================================
// Uniqueness Check
// ============================================================================

/**
 * TODO: Implement uniqueness check via Google/Bing search
 *
 * Steps:
 * 1. Perform web search for exact business name (quoted search)
 * 2. Count total search results
 * 3. Analyze top 10 results for direct business name conflicts
 * 4. Score based on result count:
 *    - < 1,000 results = 10 points (very unique)
 *    - 1,000 - 10,000 = 5 points (moderately unique)
 *    - > 10,000 = 0 points (common/generic)
 *
 * Note: Consider using Google Custom Search API or Bing Web Search API
 *
 * @param {string} businessName - The business name to check
 * @returns {Promise<Object>} Uniqueness assessment
 *   {
 *     resultCount: 2500,
 *     score: 5,
 *     topResults: [{title: '...', url: '...', snippet: '...'}],
 *     conflicts: ['Existing Company A', 'Blog named similar'],
 *     notes: 'Moderately unique name'
 *   }
 */
async function checkUniqueness(businessName) {
  console.log(`🔍 Checking uniqueness for: ${businessName}`);

  try {
    const ollamaConfig = CONFIG.apis.ollama;
    const useOllama = ollamaConfig.provider === 'ollama';

    if (useOllama) {
      const ollamaResult = await searchWithOllama(businessName);
      if (ollamaResult) {
        return calculateUniquenessScore(ollamaResult, businessName);
      }
      console.log('⚠️  Ollama uniqueness check failed, falling back to Gemini/Google/Bing');
    }

    // Prefer Gemini for web-enhanced research when available
    const geminiResult = await searchWithGemini(businessName);
    if (geminiResult) {
      return calculateUniquenessScore(geminiResult, businessName);
    }

    // Try Google Custom Search API first
    const googleResult = await searchWithGoogle(businessName);
    if (googleResult) {
      return calculateUniquenessScore(googleResult, businessName);
    }

    // Fallback to Bing Web Search API if available
    const bingResult = await searchWithBing(businessName);
    if (bingResult) {
      return calculateUniquenessScore(bingResult, businessName);
    }

    // If both APIs fail, return null result count
    return {
      resultCount: null,
      score: 0,
      topResults: [],
      conflicts: [],
      uniquenessScore: 0,
      notes: 'API services unavailable for uniqueness check'
    };

  } catch (error) {
    console.error(`❌ Error checking uniqueness for ${businessName}:`, error.message);
    return {
      resultCount: null,
      score: 0,
      topResults: [],
      conflicts: [],
      uniquenessScore: 0,
      notes: `Error occurred during uniqueness check: ${error.message}`
    };
  }
}

/**
 * Search using local Ollama model when configured
 */
async function searchWithOllama(businessName, options = {}) {
  const { endpoint, model, provider } = CONFIG.apis.ollama;

  if (provider !== 'ollama') {
    return null;
  }

  if (!endpoint) {
    console.log('⚠️  Ollama endpoint not configured');
    return null;
  }

  if (!model) {
    console.log('⚠️  Ollama model not configured');
    return null;
  }

  const url = `${endpoint}/api/generate`;
  const prompt = [
    `You are evaluating how unique the business name "${businessName}" is.`,
    'Respond ONLY with JSON matching this shape:',
    '{',
    '  "resultCount": number,',
    '  "topResults": [',
    '    {"title": string, "url": string, "snippet": string}',
    '  ],',
    '  "notes": string',
    '}',
    '',
    'If you lack web access, estimate based on general knowledge and clearly say so in "notes".',
    'Set "resultCount" to 0 when you are unsure.'
  ].join('\n');

  const requestBody = {
    model,
    prompt,
    stream: false,
    options: {
      temperature: 0.2,
      num_predict: 512
    }
  };

  try {
    console.log(`   Using Ollama model: ${model}`);
    const response = await makeHttpRequest(
      url,
      { 'Content-Type': 'application/json' },
      { method: 'POST', body: requestBody, timeout: options.timeout || 30000 }
    );

    const data = typeof response === 'string' ? safeParseJSON(response) : response;
    if (!data) {
      console.log('⚠️  Ollama returned unparseable response');
      return null;
    }

    if (data.error) {
      console.log(`⚠️  Ollama error: ${data.error}`);
      return null;
    }

    const rawOutput = typeof data.response === 'string' ? data.response.trim() : '';
    const payload = safeParseJSON(rawOutput);

    if (!payload) {
      console.log('⚠️  Ollama response is not valid JSON payload');
      return null;
    }

    const resultCount = Number.isFinite(Number(payload.resultCount))
      ? Number(payload.resultCount)
      : 0;

    const topResultsSource = Array.isArray(payload.topResults) ? payload.topResults : [];
    const topResults = topResultsSource
      .filter(item => item && (item.title || item.url))
      .slice(0, 10)
      .map(item => ({
        title: item.title || '',
        url: item.url || '',
        snippet: item.snippet || ''
      }));

    const notes = typeof payload.notes === 'string'
      ? payload.notes
      : 'Local model estimation (no live search)';

    return {
      resultCount,
      topResults,
      notes,
      provider: 'ollama',
      model
    };
  } catch (error) {
    console.log(`⚠️  Ollama request failed: ${error.message}`);
    return null;
  }
}

/**
 * Search using Gemini (with Google Search tool) to enrich uniqueness checks
 */
async function searchWithGemini(businessName, retries = 2) {
  const geminiConfig = CONFIG.apis.gemini;

  if (!geminiConfig.apiKey) {
    console.log('⚠️  Gemini API not configured');
    return null;
  }

  const candidateModels = deriveGeminiModelCandidates(geminiConfig.model);
  const prompt = `You are an analyst checking how unique a business name is. Based on your training data, estimate how many web search results would exist for the exact phrase "${businessName}". Return only JSON with this shape:
{
  "resultCount": number,          // estimated number of web results (0 if unknown)
  "topResults": [                 // up to 10 ranked results
    {"title": string, "url": string, "snippet": string}
  ],
  "notes": string                 // short insight on conflicts or notable findings
}
Provide your best estimate based on general knowledge. If unsure, set resultCount to 0 and include a helpful notes message.`;

  const requestBody = {
    contents: [
      {
        role: 'user',
        parts: [{ text: prompt }]
      }
    ],
    generationConfig: {
      temperature: 0.2,
      topP: 0.8,
      responseMimeType: 'application/json'
    }
  };

  const availabilityErrors = [];
  let lastError = null;

  outerLoop:
  for (const modelName of candidateModels) {
    const url = `${geminiConfig.endpoint}/${modelName}:generateContent?key=${geminiConfig.apiKey}`;
    console.log(`   Trying Gemini model: ${modelName}`);

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await makeHttpRequest(
          url,
          { 'Content-Type': 'application/json' },
          { method: 'POST', body: requestBody, timeout: 20000 }
        );

        if (response?.error) {
          const errorInfo = normalizeGeminiError(response.error, modelName);

          if (errorInfo.isAvailabilityIssue) {
            availabilityErrors.push(errorInfo);
            console.log(`⚠️  Gemini model ${modelName} unavailable: ${errorInfo.message}`);
            continue outerLoop;
          }

          throw new Error(errorInfo.message);
        }

        const parsedResult = parseGeminiSearchResponse(response);
        if (parsedResult) {
          console.log(`   ✅ Gemini model ${modelName} succeeded`);
          parsedResult.provider = 'gemini';
          parsedResult.model = modelName;
          return parsedResult;
        }

        console.log(`⚠️  Gemini model ${modelName} returned no structured data (attempt ${attempt}/${retries})`);
        if (attempt < retries) {
          await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
      } catch (error) {
        lastError = error;
        console.log(`⚠️  Gemini model ${modelName} attempt ${attempt} failed: ${error.message}`);
        if (attempt < retries) {
          await new Promise(resolve => setTimeout(resolve, 1500 * attempt));
        }
      }
    }
  }

  if (availabilityErrors.length > 0) {
    const triedModels = availabilityErrors.map(err => err.model).join(', ');
    console.log(`⚠️  Gemini API model availability issue. Tried models: ${triedModels}. Verify access in Google AI Studio or set GEMINI_MODEL to a permitted model (e.g. gemini-1.5-flash-latest).`);
  }

  if (lastError) {
    console.log(`⚠️  Last Gemini error: ${lastError.message}`);
  }

  return null;
}

/**
 * Parse Gemini generateContent response into search result structure
 */
function deriveGeminiModelCandidates(primaryModel) {
  const candidates = [];
  const normalized = (primaryModel || '').trim();

  if (normalized) {
    candidates.push(normalized);
  }

  if (normalized && !normalized.endsWith('-latest')) {
    candidates.push(`${normalized}-latest`);
  }

  const fallbacks = [
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro-latest',
    'gemini-1.0-pro-latest'
  ];

  fallbacks.forEach(model => {
    if (!candidates.includes(model)) {
      candidates.push(model);
    }
  });

  return candidates;
}

function normalizeGeminiError(error, modelName) {
  if (!error) {
    return {
      model: modelName,
      message: 'Unknown Gemini error',
      status: null,
      code: null,
      isAvailabilityIssue: false
    };
  }

  const status = error.status || null;
  const code = typeof error.code === 'number' || typeof error.code === 'string'
    ? error.code
    : null;

  const details = Array.isArray(error.details)
    ? error.details
        .map(detail => {
          if (typeof detail === 'string') {
            return detail;
          }
          if (detail?.reason) {
            return detail.reason;
          }
          if (detail?.message) {
            return detail.message;
          }
          return JSON.stringify(detail);
        })
        .filter(Boolean)
    : [];

  let message = typeof error === 'string'
    ? error
    : error.message || 'Gemini API error';

  if (details.length > 0) {
    message = `${message} (${details.join('; ')})`;
  }

  const messageLower = message.toLowerCase();
  const isAvailabilityIssue =
    status === 'NOT_FOUND' ||
    status === 'FAILED_PRECONDITION' && messageLower.includes('location') ||
    status === 'PERMISSION_DENIED' && messageLower.includes('restricted') ||
    code === 403 && messageLower.includes('not available') ||
    code === 404 ||
    messageLower.includes('not found') ||
    messageLower.includes('not available') ||
    messageLower.includes('available in region') ||
    messageLower.includes('support the request location') ||
    messageLower.includes('model') && messageLower.includes('available');

  return {
    model: modelName,
    message,
    status,
    code,
    isAvailabilityIssue
  };
}

function parseGeminiSearchResponse(response) {
  const data = typeof response === 'string' ? safeParseJSON(response) : response;

  if (!data || data.error) {
    if (data?.error?.message) {
      console.log('⚠️  Gemini API error:', data.error.message);
    }
    return null;
  }

  const candidates = Array.isArray(data.candidates) ? data.candidates : [];
  for (const candidate of candidates) {
    const parts = candidate?.content?.parts || [];

    for (const part of parts) {
      const payload =
        typeof part.text === 'string' ? safeParseJSON(part.text) :
        part?.functionCall?.args ? part.functionCall.args :
        part?.structValue ? part.structValue :
        null;

      if (!payload) {
        continue;
      }

      if (payload.error) {
        const message = typeof payload.error === 'string'
          ? payload.error
          : payload.error.message || JSON.stringify(payload.error);
        console.log('⚠️  Gemini payload reported error:', message);
        continue;
      }

      const resultCountRaw =
        payload.resultCount ??
        payload.totalResults ??
        payload.estimatedResults ??
        payload.totalMatches ??
        null;

      const resultCount = Number.isFinite(Number(resultCountRaw))
        ? Number(resultCountRaw)
        : 0;

      const topResultsSource =
        Array.isArray(payload.topResults) ? payload.topResults :
        Array.isArray(payload.results) ? payload.results :
        [];

      const topResults = topResultsSource
        .filter(item => item && (item.title || item.url))
        .slice(0, 10)
        .map(item => ({
          title: item.title || item.name || '',
          url: item.url || item.link || '',
          snippet: item.snippet || item.description || item.summary || ''
        }));

      return {
        resultCount,
        topResults,
        notes: typeof payload.notes === 'string'
          ? payload.notes
          : (typeof payload.summary === 'string' ? payload.summary : undefined)
      };
    }
  }

  return null;
}

/**
 * Search using Google Custom Search API with retry logic
 */
async function searchWithGoogle(businessName, retries = 3) {
  const apiKey = process.env.GOOGLE_SEARCH_API_KEY;
  const searchEngineId = process.env.GOOGLE_SEARCH_ENGINE_ID;

  if (!apiKey || !searchEngineId) {
    console.log('⚠️  Google Custom Search API not configured');
    return null;
  }

  const searchQuery = `"${businessName}"`;
  const url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=${encodeURIComponent(searchQuery)}`;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await makeHttpRequest(url);
      
      if (response.error) {
        if (response.error.code === 429) {
          // Rate limit - wait and retry
          const waitTime = Math.pow(2, attempt) * 1000; // Exponential backoff
          console.log(`⏳ Rate limited, waiting ${waitTime}ms before retry ${attempt}/${retries}`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }
        throw new Error(`Google API error: ${response.error.message}`);
      }

      return {
        resultCount: parseInt(response.searchInformation?.totalResults || '0'),
        topResults: (response.items || []).slice(0, 10).map(item => ({
          title: item.title,
          url: item.link,
          snippet: item.snippet
        }))
      };

    } catch (error) {
      console.log(`⚠️  Google search attempt ${attempt} failed:`, error.message);
      if (attempt === retries) {
        throw error;
      }
      // Wait before retry
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }

  return null;
}

/**
 * Search using Bing Web Search API as fallback
 */
async function searchWithBing(businessName, retries = 2) {
  const apiKey = process.env.BING_SEARCH_API_KEY;

  if (!apiKey) {
    console.log('⚠️  Bing Web Search API not configured');
    return null;
  }

  const searchQuery = `"${businessName}"`;
  const url = `https://api.bing.microsoft.com/v7.0/search?q=${encodeURIComponent(searchQuery)}`;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await makeHttpRequest(url, {
        'Ocp-Apim-Subscription-Key': apiKey
      });

      if (response.error) {
        throw new Error(`Bing API error: ${response.error.message}`);
      }

      return {
        resultCount: parseInt(response.webPages?.totalEstimatedMatches || '0'),
        topResults: (response.webPages?.value || []).slice(0, 10).map(item => ({
          title: item.name,
          url: item.url,
          snippet: item.snippet
        }))
      };

    } catch (error) {
      console.log(`⚠️  Bing search attempt ${attempt} failed:`, error.message);
      if (attempt === retries) {
        throw error;
      }
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }

  return null;
}

/**
 * Calculate uniqueness score based on search result count
 */
function calculateUniquenessScore(searchResult, businessName) {
  const resultCount = searchResult.resultCount || 0;
  let uniquenessScore = 0;
  let note = '';

  // Apply scoring curve
  if (resultCount === 0) {
    uniquenessScore = 30;
    note = 'No search results found - extremely unique name';
  } else if (resultCount >= 1 && resultCount <= 100) {
    uniquenessScore = 25;
    note = 'Very low search footprint - highly unique';
  } else if (resultCount >= 101 && resultCount <= 1000) {
    uniquenessScore = 15;
    note = 'Low search footprint - moderately unique';
  } else if (resultCount >= 1001 && resultCount <= 10000) {
    uniquenessScore = 8;
    note = 'Moderate presence - some uniqueness concerns';
  } else {
    uniquenessScore = 0;
    note = 'High search presence - may have conflicts';
  }

  // Analyze top results for conflicts
  const conflicts = analyzeConflicts(searchResult.topResults || [], businessName);
  const additionalInsight = searchResult.notes
    ? ` Additional insight: ${searchResult.notes}`
    : '';
  const providerSuffix = searchResult.provider
    ? ` Source: ${searchResult.provider}${searchResult.model ? ` (${searchResult.model})` : ''}`
    : '';

  return {
    resultCount,
    uniquenessScore,
    note,
    score: uniquenessScore, // For backward compatibility
    topResults: searchResult.topResults || [],
    conflicts,
    notes: `${note} (${resultCount.toLocaleString()} search results)${additionalInsight}${providerSuffix}`
  };
}

/**
 * Analyze top search results for potential conflicts
 */
function analyzeConflicts(topResults, businessName) {
  const conflicts = [];
  const nameLower = businessName.toLowerCase();

  topResults.forEach(result => {
    const titleLower = result.title.toLowerCase();
    const snippetLower = (result.snippet || '').toLowerCase();

    // Check for exact business name matches
    if (titleLower.includes(nameLower) || snippetLower.includes(nameLower)) {
      conflicts.push({
        type: 'exact_match',
        title: result.title,
        url: result.url,
        snippet: result.snippet
      });
    }
    // Check for similar business names
    else if (isSimilarBusinessName(titleLower, nameLower)) {
      conflicts.push({
        type: 'similar_name',
        title: result.title,
        url: result.url,
        snippet: result.snippet
      });
    }
  });

  return conflicts;
}

/**
 * Check if two business names are similar
 */
function isSimilarBusinessName(name1, name2) {
  // Simple similarity check - can be enhanced with more sophisticated algorithms
  const words1 = name1.split(/\s+/);
  const words2 = name2.split(/\s+/);
  
  let commonWords = 0;
  words1.forEach(word => {
    if (words2.includes(word) && word.length > 2) {
      commonWords++;
    }
  });

  return commonWords >= Math.min(words1.length, words2.length) * 0.5;
}

function safeParseJSON(value) {
  if (typeof value !== 'string') {
    return null;
  }
  try {
    return JSON.parse(value);
  } catch (error) {
    return null;
  }
}

/**
 * Make HTTP request with timeout and error handling
 */
async function makeHttpRequest(url, headers = {}, options = {}) {
  const https = require('https');
  const http = require('http');
  const { URL } = require('url');

  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const isHttps = urlObj.protocol === 'https:';
    const requestModule = isHttps ? https : http;
    
    const requestOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || (isHttps ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: {
        'Accept': 'application/json,text/html,*/*',
        'User-Agent': 'NameVettingBot/1.0',
        ...headers
      },
      timeout: options.timeout || 10000
    };

    let requestBody = null;
    if (options.body !== undefined && options.body !== null) {
      requestBody = typeof options.body === 'string'
        ? options.body
        : JSON.stringify(options.body);

      if (!requestOptions.headers['Content-Type']) {
        requestOptions.headers['Content-Type'] = 'application/json';
      }

      requestOptions.headers['Content-Length'] = Buffer.byteLength(requestBody);
    }

    const req = requestModule.request(requestOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        // For social media checks, return both status and body
        if (options.returnBody) {
          resolve({
            status: res.statusCode,
            body: data,
            headers: res.headers
          });
        } else {
          // For API calls, try to parse JSON
          try {
            resolve(JSON.parse(data));
          } catch (error) {
            // If JSON parsing fails, return the raw data
            resolve(data);
          }
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (requestBody) {
      req.end(requestBody);
    } else {
      req.end();
    }
  });
}

// ============================================================================
// Scoring & Reporting
// ============================================================================

/**
 * Calculate total score and risk assessment
 *
 * @param {Object} results - All check results
 * @returns {Object} Scored assessment
 */
function calculateTotalScore(results) {
  const { domain, trademark, social, uniqueness } = results;

  const totalScore = (domain?.score || 0) +
                     (trademark?.score || 0) +
                     (social?.score || 0) +
                     (uniqueness?.score || 0);

  let assessment = 'AVOID';
  let recommendation = 'High risk - consider alternative names';

  if (totalScore >= CONFIG.thresholds.excellent) {
    assessment = 'EXCELLENT';
    recommendation = 'Strong name candidate - proceed with confidence';
  } else if (totalScore >= CONFIG.thresholds.good) {
    assessment = 'GOOD';
    recommendation = 'Viable option - minor concerns to address';
  } else if (totalScore >= CONFIG.thresholds.risky) {
    assessment = 'RISKY';
    recommendation = 'Significant concerns - additional research needed';
  }

  return {
    totalScore,
    maxScore: 100,
    percentage: Math.round((totalScore / 100) * 100),
    assessment,
    recommendation,
    breakdown: {
      domain: `${domain?.score || 0}/${CONFIG.scoring.domainAvailability}`,
      trademark: `${trademark?.score || 0}/${CONFIG.scoring.trademarkRisk}`,
      social: `${social?.score || 0}/${CONFIG.scoring.socialAvailability}`,
      uniqueness: `${uniqueness?.score || 0}/${CONFIG.scoring.uniqueness}`,
    }
  };
}

/**
 * Generate comprehensive vetting report
 *
 * @param {string} businessName - Business name
 * @param {Object} results - All check results
 * @returns {Object} Complete report
 */
function generateReport(businessName, results) {
  const scoring = calculateTotalScore(results);

  return {
    name: businessName,
    timestamp: new Date().toISOString(),
    score: scoring,
    details: {
      domain: results.domain,
      trademark: results.trademark,
      social: results.social,
      uniqueness: results.uniqueness,
    },
    summary: {
      pros: extractPros(results),
      cons: extractCons(results),
      actionItems: generateActionItems(results, scoring),
    }
  };
}

/**
 * Extract positive points from results
 */
function extractPros(results) {
  const pros = [];

  if (results.domain?.score >= 30) {
    pros.push(`Premium domain available: ${results.domain.bestDomain}`);
  }
  if (results.trademark?.riskLevel === 'low') {
    pros.push('No trademark conflicts detected');
  }
  if (results.social?.availableCount >= 2) {
    pros.push(`${results.social.availableCount}/3 social handles available`);
  }
  if (results.uniqueness?.score >= 5) {
    pros.push('Name has good uniqueness/searchability');
  }

  return pros.length > 0 ? pros : ['None identified'];
}

/**
 * Extract concerns from results
 */
function extractCons(results) {
  const cons = [];

  if (results.domain?.score < 20) {
    cons.push('Limited domain availability - may need alternative TLD');
  }
  if (results.trademark?.riskLevel === 'high') {
    cons.push('⚠️  Trademark conflict detected - legal review required');
  }
  if (results.social?.availableCount < 2) {
    cons.push('Limited social handle availability');
  }
  if (results.uniqueness?.score === 0) {
    cons.push('Name may be too generic or commonly used');
  }

  return cons.length > 0 ? cons : ['None identified'];
}

/**
 * Generate recommended action items
 */
function generateActionItems(results, scoring) {
  const actions = [];

  if (scoring.assessment === 'EXCELLENT') {
    actions.push('✅ Proceed to domain registration');
    actions.push('✅ Secure available social handles immediately');
    actions.push('Consider trademark registration for brand protection');
  } else if (scoring.assessment === 'GOOD') {
    actions.push('Review and address minor concerns');
    actions.push('Consider trademark attorney consultation');
    actions.push('Explore alternative domain/handle options as backup');
  } else if (scoring.assessment === 'RISKY') {
    actions.push('⚠️  Deep dive into trademark conflicts');
    actions.push('Research alternative name variations');
    actions.push('Consult legal team before proceeding');
  } else {
    actions.push('🛑 Select alternative name');
    actions.push('Run vetting process on backup options');
  }

  return actions;
}

// ============================================================================
// Main Execution
// ============================================================================

/**
 * Vet a single business name
 *
 * @param {string} businessName - Name to vet
 * @param {Object} options - Vetting options
 * @returns {Promise<Object>} Vetting report
 */
async function vetBusinessName(businessName, options = {}) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`🔎 VETTING: ${businessName}`);
  console.log(`${'='.repeat(60)}\n`);

  const results = {};

  try {
    // Run all checks
    results.domain = await checkDomainAvailability(businessName);
    results.trademark = await checkTrademarkConflicts(businessName, options.industry);
    results.social = await checkSocialHandles(businessName);
    results.uniqueness = await checkUniqueness(businessName);

    // Generate report
    const report = generateReport(businessName, results);

    // Display summary
    console.log(`\n📊 SCORE: ${report.score.totalScore}/100 (${report.score.assessment})`);
    console.log(`   ${report.score.recommendation}\n`);

    return report;

  } catch (error) {
    console.error(`❌ Error vetting name "${businessName}":`, error.message);
    throw error;
  }
}

/**
 * Vet multiple business names and rank them
 */
async function vetMultipleNames(names, options = {}) {
  const reports = [];

  for (const name of names) {
    const report = await vetBusinessName(name, options);
    reports.push(report);
  }

  // Sort by score (highest first)
  reports.sort((a, b) => b.score.totalScore - a.score.totalScore);

  // Display ranking
  console.log(`\n${'='.repeat(60)}`);
  console.log('📊 NAME RANKING');
  console.log(`${'='.repeat(60)}\n`);

  reports.forEach((report, index) => {
    console.log(`${index + 1}. ${report.name}`);
    console.log(`   Score: ${report.score.totalScore}/100 (${report.score.assessment})`);
    console.log(`   Domain: ${report.details.domain?.bestDomain || 'N/A'}`);
    console.log('');
  });

  return reports;
}

/**
 * CLI argument parsing
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    names: [],
    input: null,
    output: null,
    industry: null,
    deepCheck: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--names' && args[i + 1]) {
      options.names = args[i + 1].split(',').map(n => n.trim());
      i++;
    } else if (arg === '--name' && args[i + 1]) {
      options.names = [args[i + 1]];
      i++;
    } else if (arg === '--input' && args[i + 1]) {
      options.input = args[i + 1];
      i++;
    } else if (arg === '--output' && args[i + 1]) {
      options.output = args[i + 1];
      i++;
    } else if (arg === '--industry' && args[i + 1]) {
      options.industry = args[i + 1];
      i++;
    } else if (arg === '--deep-check') {
      options.deepCheck = true;
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    }
  }

  return options;
}

/**
 * Print help message
 */
function printHelp() {
  console.log(`
Name Vetting Automation
=======================

Usage:
  node scripts/name-vetting.js [options]

Options:
  --names <comma-separated>  Check multiple names
  --name <single-name>       Check a single name
  --input <file>             Read names from JSON file
  --output <file>            Save report to JSON file
  --industry <industry>      Specify industry for trademark search
  --deep-check               Run extended checks (slower, more thorough)
  --help, -h                 Show this help message

Examples:
  node scripts/name-vetting.js --names "Acme Corp,Widget Labs,Tech Solutions"
  node scripts/name-vetting.js --name "Acme Corp" --industry "Software"
  node scripts/name-vetting.js --input names.json --output vetting-report.json

Environment Variables:
  DOMAINR_API_KEY           API key for Domainr
  GODADDY_API_KEY           API key for GoDaddy
  GODADDY_API_SECRET        API secret for GoDaddy
  USPTO_API_KEY             API key for USPTO
  GEMINI_API_KEY            Google AI Studio API key for Gemini search
  GEMINI_MODEL              Optional Gemini model (defaults to gemini-1.5-flash-latest)
  UNIQUE_CHECK_PROVIDER     Set to 'ollama' to prefer local processing
  OLLAMA_ENDPOINT           Optional Ollama endpoint (default http://127.0.0.1:11434)
  OLLAMA_MODEL              Ollama model name (default llama3)
  GOOGLE_SEARCH_API_KEY     API key for Google Custom Search
  GOOGLE_SEARCH_ENGINE_ID   Search engine ID for Google Custom Search
  BING_SEARCH_API_KEY       API key for Bing Web Search

Scoring:
  Domain Availability:   0-40 points
  Trademark Risk:        0-30 points
  Social Availability:   0-20 points
  Uniqueness:           0-30 points
  -------------------------
  Total:                0-120 points

  84-120: EXCELLENT - Strong candidate
  60-83:  GOOD - Viable option
  36-59:  RISKY - Significant concerns
  0-35:   AVOID - High risk
`);
}

/**
 * Main entry point
 */
async function main() {
  const options = parseArgs();

  // Load names from input file if specified
  if (options.input) {
    try {
      const inputData = JSON.parse(fs.readFileSync(options.input, 'utf8'));
      options.names = Array.isArray(inputData) ? inputData : inputData.names || [];
    } catch (error) {
      console.error(`❌ Error reading input file: ${error.message}`);
      process.exit(1);
    }
  }

  // Validate we have names to check
  if (options.names.length === 0) {
    console.error('❌ No names specified. Use --names, --name, or --input.');
    console.error('   Run with --help for usage information.');
    process.exit(1);
  }

  console.log(`\n🚀 Name Vetting Automation Starting...`);
  console.log(`   Checking ${options.names.length} name(s)\n`);

  // Vet all names
  const reports = await vetMultipleNames(options.names, options);

  // Save output if specified
  if (options.output) {
    try {
      fs.writeFileSync(
        options.output,
        JSON.stringify(reports, null, 2),
        'utf8'
      );
      console.log(`\n✅ Report saved to: ${options.output}`);
    } catch (error) {
      console.error(`❌ Error saving report: ${error.message}`);
      process.exit(1);
    }
  }

  console.log(`\n✅ Name vetting complete!\n`);
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Fatal error:', error);
    process.exit(1);
  });
}

// Export functions for use as module
module.exports = {
  vetBusinessName,
  vetMultipleNames,
  checkDomainAvailability,
  checkTrademarkConflicts,
  checkSocialHandles,
  checkUniqueness,
  searchWithGemini,
  searchWithOllama,
  calculateTotalScore,
  generateReport,
  // Helper functions for testing
  calculateTrademarkSimilarity,
  normalizeToTrademark,
  levenshteinDistance,
};
