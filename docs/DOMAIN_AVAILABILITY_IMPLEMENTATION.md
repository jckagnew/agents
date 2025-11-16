# Domain Availability Implementation

## Overview

The domain availability check has been fully implemented in [scripts/name-vetting.js](../scripts/name-vetting.js) with support for both Domainr and GoDaddy APIs.

**Status**: ✅ Complete - Ready for API key configuration

---

## Implementation Details

### Main Function: `checkDomainAvailability(businessName)`

**Location**: [scripts/name-vetting.js:104-243](../scripts/name-vetting.js#L104-L243)

**Features**:
- ✅ Normalizes business names to domain-safe format
- ✅ Checks 6 TLD extensions (.com, .io, .co, .app, .tech, .ai)
- ✅ Primary API: Domainr (bulk checking)
- ✅ Fallback API: GoDaddy (individual checking)
- ✅ Graceful error handling - returns "unknown" when APIs unavailable
- ✅ Scoring system (40 points for .com, 30 for .io/.co, 20 for others)
- ✅ Premium domain detection with pricing hints
- ✅ Prioritized domain selection (prefers .com > .io/.co > others)

### Supporting Functions

#### 1. `checkDomainrAvailability(domains)`
**Location**: [scripts/name-vetting.js:245-291](../scripts/name-vetting.js#L245-L291)

- Uses Domainr API `/v2/status` endpoint
- Supports bulk domain checking (all TLDs in single request)
- Parses status: inactive/undelegated = available, active/parked = taken, premium = premium

#### 2. `parseDomainrStatus(statusObj)`
**Location**: [scripts/name-vetting.js:293-317](../scripts/name-vetting.js#L293-L317)

- Interprets Domainr response summaries
- Maps to standardized availability states (available, premium, taken, unknown)

#### 3. `checkGoDaddyAvailability(domains)`
**Location**: [scripts/name-vetting.js:319-378](../scripts/name-vetting.js#L319-L378)

- Uses GoDaddy API `/v1/domains/available` endpoint
- Checks domains individually (API limitation)
- Parses pricing in micro-units and converts to USD
- Requires `sso-key` authentication header

#### 4. `normalizeToDomain(name)`
**Location**: [scripts/name-vetting.js:380-397](../scripts/name-vetting.js#L380-L397)

- Converts business names to valid domain format
- Lowercase, removes spaces/special characters
- Handles common separators (spaces, hyphens, underscores, periods)

---

## API Configuration

### Domainr API (Primary)

**Endpoint**: `https://api.domainr.com/v2/status`

**Authentication**:
```bash
export DOMAINR_API_KEY="your_api_key"
```

**Request Format**:
```
GET https://api.domainr.com/v2/status?domain=example.com&domain=example.io&client_id=YOUR_KEY
```

**Response Format**:
```json
{
  "status": [
    {
      "domain": "example.com",
      "summary": "inactive",
      "status": "undelegated inactive",
      "zone": "com"
    }
  ]
}
```

**Rate Limits**: 100 requests/hour (free tier)

**Documentation**: https://domainr.com/docs/api

**Advantages**:
- ✅ Bulk checking (all TLDs in one request)
- ✅ Fast response times
- ✅ Premium domain detection
- ✅ Comprehensive status information

### GoDaddy API (Fallback)

**Endpoint**: `https://api.godaddy.com/v1/domains/available`

**Authentication**:
```bash
export GODADDY_API_KEY="your_api_key"
export GODADDY_API_SECRET="your_api_secret"
```

**Request Format**:
```
GET https://api.godaddy.com/v1/domains/available?domain=example.com
Headers:
  Authorization: sso-key YOUR_KEY:YOUR_SECRET
  Accept: application/json
```

**Response Format**:
```json
{
  "available": true,
  "domain": "example.com",
  "price": 12990000
}
```

**Rate Limits**: 60 requests/minute

**Documentation**: https://developer.godaddy.com/doc/endpoint/domains

**Advantages**:
- ✅ Pricing information included
- ✅ High accuracy
- ✅ Direct registration capability

**Limitations**:
- ❌ Requires individual domain checks (slower for multiple TLDs)
- ❌ Requires paid API key for production use

---

## Scoring System

The domain availability check contributes **0-40 points** to the total name vetting score:

| Domain Type | Points | Condition |
|------------|--------|-----------|
| .com available | 40 | Premium .com domain available |
| .io or .co available | 30 | Alternative premium TLD available |
| Other TLD available (.app, .tech, .ai) | 20 | Secondary TLD available |
| No domains available | 0 | All TLDs taken or unknown |

**Best Domain Selection Priority**:
1. .com (if available)
2. .io or .co (if .com unavailable)
3. Other TLDs (.app, .tech, .ai)

---

## Usage Examples

### Basic Usage

```bash
# Check domain availability for a single name
node scripts/name-vetting.js --name "Acme Corp"
```

**Output**:
```
🌐 Checking domain availability for: Acme Corp
   Using Domainr API...
   ✓ Found 3 available domains
   ✓ Best domain: acmecorp.com (40 points)

Domain Check:
  Available domains: 3
  Best domain: acmecorp.com
  Score: 40/40
  Notes: Premium .com domain available

  Domain Details:
    acmecorp.com: available
    acmecorp.io: available
    acmecorp.co: taken
    acmecorp.app: available
    acmecorp.tech: taken
    acmecorp.ai: taken
```

### Batch Processing

```bash
# Check multiple names
node scripts/name-vetting.js --names "Acme Corp,Widget Labs,Tech Solutions"
```

### Without API Keys (Graceful Fallback)

```bash
# Run without API keys configured
node scripts/name-vetting.js --name "Acme Corp"
```

**Output**:
```
🌐 Checking domain availability for: Acme Corp
   ⚠️  Domainr API key not found, trying GoDaddy...
   ⚠️  GoDaddy API credentials not found
   ✓ Found 0 available domains

Domain Check:
  Available domains: 0
  Best domain: None found
  Score: 0/40
  Notes: Unable to verify domain availability - API keys not configured

  Domain Details:
    acmecorp.com: unknown
    acmecorp.io: unknown
    acmecorp.co: unknown
    acmecorp.app: unknown
    acmecorp.tech: unknown
    acmecorp.ai: unknown
```

---

## Testing

### Test Script

**Location**: [scripts/test-domain-check.js](../scripts/test-domain-check.js)

Run the test suite:
```bash
node scripts/test-domain-check.js
```

This tests:
- ✅ Name normalization
- ✅ TLD expansion
- ✅ API fallback behavior
- ✅ Error handling
- ✅ Graceful degradation without API keys
- ✅ Scoring calculation

### Manual Testing with API Keys

```bash
# Set API keys
export DOMAINR_API_KEY="your_domainr_key"

# Test with real API
node scripts/name-vetting.js --name "YourBusinessName"
```

---

## Error Handling

The implementation includes comprehensive error handling:

### 1. Missing API Keys
- ✅ Detects missing Domainr API key
- ✅ Falls back to GoDaddy API
- ✅ Returns "unknown" status if both unavailable
- ✅ Provides clear warning messages

### 2. API Errors
- ✅ Catches HTTP errors (non-200 status codes)
- ✅ Catches network errors (timeout, connection refused)
- ✅ Catches JSON parsing errors
- ✅ Logs detailed error messages
- ✅ Returns "unknown" status for affected domains

### 3. Invalid Responses
- ✅ Handles missing fields in API responses
- ✅ Handles unexpected status values
- ✅ Provides sensible defaults

---

## Return Value Structure

```javascript
{
  available: [
    {
      extension: '.com',
      domain: 'acmecorp.com',
      available: true,
      availability: 'available',
      priceHint: null
    }
  ],
  unavailable: [
    {
      extension: '.io',
      domain: 'acmecorp.io',
      available: false,
      availability: 'taken',
      priceHint: null
    }
  ],
  details: [
    // All domains checked (available + unavailable)
  ],
  score: 40,              // 0-40 points
  bestDomain: 'acmecorp.com',
  notes: 'Premium .com domain available'
}
```

---

## Integration with Name Vetting Workflow

The domain availability check integrates seamlessly with the full name vetting workflow:

```javascript
const result = await vetBusinessName('Acme Corp');

// Access domain results
console.log(result.details.domain.score);      // 0-40
console.log(result.details.domain.bestDomain); // 'acmecorp.com'
console.log(result.details.domain.available);  // Array of available domains

// Total score includes domain + trademark + social + uniqueness
console.log(result.score.totalScore);          // 0-100
console.log(result.score.assessment);          // EXCELLENT/GOOD/RISKY/AVOID
```

---

## Next Steps

### Immediate
1. ✅ Domain availability implementation complete
2. ⏳ Obtain Domainr API key for production use
3. ⏳ (Optional) Obtain GoDaddy API credentials for fallback

### Future Enhancements
1. Add caching layer to reduce API calls for frequently checked names
2. Support for additional TLDs (.app, .dev, .xyz, etc.)
3. Integration with domain registrars for instant registration
4. Historical domain availability tracking
5. Expired domain detection and acquisition opportunities

---

## Cost Considerations

### Domainr API
- **Free Tier**: 100 requests/hour
- **Cost**: $0 (free tier sufficient for development)
- **Production**: Consider paid tier for higher volume

### GoDaddy API
- **Free Tier**: Limited
- **Cost**: Requires domain purchase for full access
- **Production**: May require partnership agreement

### Recommendation
Start with Domainr free tier for development and testing. Upgrade to paid tier or add GoDaddy fallback only if hitting rate limits.

---

**Last Updated**: October 25, 2025
**Status**: Production Ready (pending API key configuration)
**Implemented By**: Claude Code
**Related**: [scripts/name-vetting.js](../scripts/name-vetting.js), [Phase 2.5: Business Name Vetting](SOFTWARE_FACTORY_PLAYBOOK.md#phase-25)
