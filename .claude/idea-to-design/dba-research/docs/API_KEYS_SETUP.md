# Name Vetting API Keys Setup Guide

**Purpose**: Configure API keys for automated DBA name vetting services  
**Last Updated**: October 25, 2025  
**Status**: Ready for Implementation  

## Overview

This guide walks through setting up API keys for the four name vetting services used in the DBA naming automation pipeline. These services provide domain availability, trademark search, and brand conflict detection capabilities.

---

## 🔑 Required API Keys

### Primary Services (Required)
1. **Domainr API** - Domain availability and registration data
2. **Google Custom Search API** - Brand conflict detection via web search
3. **USPTO TSDR API** - Trademark search (no API key required)

### Fallback Services (Optional)
4. **GoDaddy API** - Domain availability fallback

---

## 📋 Setup Instructions

### 1. Domainr API

**Purpose**: Primary domain availability and registration data  
**Pricing**: Free tier (100 requests/month), Paid ($10/month for 10,000 requests)  
**Priority**: 1 (Primary)

#### Setup Steps:
1. **Visit**: https://domainr.com/
2. **Sign up** for a free account
3. **Navigate** to API section in dashboard
4. **Generate** API key
5. **Add to environment**: `DOMAINR_API_KEY=your-key-here`

#### API Features:
- Domain availability check
- Domain registration status
- Domain suggestions
- TLD information

---

### 2. Google Custom Search API

**Purpose**: Web search for brand conflicts and mentions  
**Pricing**: Free tier (100 requests/day), Paid ($5 per 1,000 requests)  
**Priority**: 1 (Primary)

#### Setup Steps:
1. **Visit**: https://console.developers.google.com/
2. **Create** new project or select existing
3. **Enable** Custom Search API
4. **Create** credentials (API key)
5. **Create Custom Search Engine**: https://cse.google.com/
6. **Get Search Engine ID** from CSE settings
7. **Add to environment**:
   - `GOOGLE_SEARCH_API_KEY=your-key-here`
   - `GOOGLE_SEARCH_ENGINE_ID=your-engine-id-here`

#### API Features:
- Web search for brand mentions
- Competitor analysis
- Brand conflict detection
- Social media mentions

---

### 3. USPTO TSDR API

**Purpose**: Trademark search and status data  
**Pricing**: Free  
**Priority**: 1 (Primary)

#### Setup Steps:
1. **No API key required** for USPTO TSDR
2. **Use direct API calls** to `tsdrapi.uspto.gov`
3. **Implement rate limiting** (1 request/second recommended)
4. **Handle response parsing** for trademark data

#### API Features:
- Trademark search
- Trademark status
- Trademark owner information
- Trademark class information

---

### 4. GoDaddy API (Fallback)

**Purpose**: Domain availability fallback service  
**Pricing**: Free tier (1,000 requests/month), Paid ($0.01 per request)  
**Priority**: 2 (Fallback)

#### Setup Steps:
1. **Visit**: https://developer.godaddy.com/
2. **Sign up** for developer account
3. **Create** new application
4. **Generate** API key and secret
5. **Add to environment**:
   - `GODADDY_API_KEY=your-key-here`
   - `GODADDY_SECRET_KEY=your-secret-here`

#### API Features:
- Domain availability check
- Domain registration
- Domain pricing
- Domain suggestions

---

## 🔧 Environment Configuration

### Required Variables
```bash
# Primary Services
DOMAINR_API_KEY=your-domainr-api-key
GOOGLE_SEARCH_API_KEY=your-google-search-api-key
GOOGLE_SEARCH_ENGINE_ID=your-google-search-engine-id
```

### Optional Variables
```bash
# Fallback Services
GODADDY_API_KEY=your-godaddy-api-key
GODADDY_SECRET_KEY=your-godaddy-secret-key
```

### Environment File Setup
1. **Copy** `env.template` to `.env`
2. **Fill in** the API keys above
3. **Never commit** `.env` files to version control

---

## 🚀 Testing API Keys

### Test Script
Create a test script to verify all API keys are working:

```javascript
// test-api-keys.js
const config = require('./config/api-keys.json');

async function testAPIKeys() {
  console.log('🔑 Testing Name Vetting API Keys...');
  
  // Test Domainr API
  if (process.env.DOMAINR_API_KEY) {
    console.log('✅ Domainr API key configured');
  } else {
    console.log('❌ Domainr API key missing');
  }
  
  // Test Google Search API
  if (process.env.GOOGLE_SEARCH_API_KEY && process.env.GOOGLE_SEARCH_ENGINE_ID) {
    console.log('✅ Google Search API configured');
  } else {
    console.log('❌ Google Search API missing');
  }
  
  // Test GoDaddy API (optional)
  if (process.env.GODADDY_API_KEY && process.env.GODADDY_SECRET_KEY) {
    console.log('✅ GoDaddy API configured (fallback)');
  } else {
    console.log('⚠️  GoDaddy API not configured (optional)');
  }
  
  console.log('✅ USPTO API ready (no key required)');
}

testAPIKeys();
```

### Run Test
```bash
node test-api-keys.js
```

---

## 📊 Rate Limits & Usage

### Service Limits
| Service | Free Tier | Paid Tier | Rate Limit |
|---------|-----------|-----------|------------|
| **Domainr** | 100 requests/month | 10,000 requests/month | 1 request/second |
| **Google Search** | 100 requests/day | 10,000 requests/day | 1 request/second |
| **USPTO** | Unlimited | N/A | 1 request/second (recommended) |
| **GoDaddy** | 1,000 requests/month | Unlimited | 1 request/second |

### Usage Optimization
- **Batch requests** when possible
- **Cache results** to reduce API calls
- **Use fallback services** for high-volume operations
- **Monitor usage** to stay within limits

---

## 🔒 Security Best Practices

### API Key Management
1. **Never commit** API keys to version control
2. **Use environment variables** for all keys
3. **Rotate keys** regularly (quarterly)
4. **Monitor usage** for unauthorized access
5. **Use different keys** for development/production

### Environment Security
```bash
# .env file permissions
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

---

## 🛠️ Integration Examples

### Domain Availability Check
```javascript
// Using Domainr API
const domainr = require('domainr');
const result = await domainr.status('example.com', {
  key: process.env.DOMAINR_API_KEY
});
```

### Trademark Search
```javascript
// Using USPTO TSDR API
const uspto = require('uspto-tsdr');
const result = await uspto.search('EXAMPLE', {
  rateLimit: 1000 // 1 second delay
});
```

### Brand Conflict Search
```javascript
// Using Google Custom Search API
const google = require('googleapis');
const customsearch = google.customsearch('v1');
const result = await customsearch.cse.list({
  auth: process.env.GOOGLE_SEARCH_API_KEY,
  cx: process.env.GOOGLE_SEARCH_ENGINE_ID,
  q: 'brand name conflict search'
});
```

---

## 📞 Support & Troubleshooting

### Common Issues
1. **API Key Invalid**: Verify key is correctly copied
2. **Rate Limit Exceeded**: Implement proper rate limiting
3. **CORS Issues**: Configure proper headers
4. **Authentication Failed**: Check key permissions

### Service Status
- **Domainr**: https://status.domainr.com/
- **Google APIs**: https://status.cloud.google.com/
- **USPTO**: https://www.uspto.gov/trademarks-application-process/search-trademark-database
- **GoDaddy**: https://developer.godaddy.com/status

### Documentation Links
- **Domainr API**: https://domainr.com/docs
- **Google Custom Search**: https://developers.google.com/custom-search/v1/introduction
- **USPTO TSDR**: https://www.uspto.gov/trademarks-application-process/search-trademark-database
- **GoDaddy API**: https://developer.godaddy.com/doc

---

**Next Steps**: After setting up API keys, proceed to configure the name vetting automation pipeline.

**Related Files**:
- `.claude/idea-to-design/dba-research/config/api-keys.json`
- `env.template`
- `.claude/idea-to-design/dba-research/filtered/dba-candidates-round2.json`
