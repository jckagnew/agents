# API Specification

## Overview


HydroTrack is a **local-first application** with no backend API in the MVP.

**Decision**: No API endpoints required for core functionality
**Rationale**: All 3 must-have features work offline with localStorage

**Future Consideration**: API may be added if users request:
- Cloud sync across devices
- Team collaboration features
- Analytics beyond local data


---


## No API Required

HydroTrack operates entirely client-side with no backend API.

**Data Flow**:
```
User Action → React State → localStorage → UI Update
```

**Benefits**:
- ✅ Zero latency (no network calls)
- ✅ Offline-first (always works)
- ✅ Privacy (no data leaves device)
- ✅ Cost (no server hosting)

**If API Added Later**:
Would follow REST conventions:
- `POST /api/sync` - Cloud sync
- `GET /api/export` - Data export
- `POST /api/auth/login` - Authentication

See `architecture-tech-stack.md` for migration path.


---

## External Integrations

### Current (MVP)
**None** - No third-party API dependencies

### Future Consideration


#### Apple Health / Google Fit
**Purpose**: Import health data from wearables

**Implementation**:
- OAuth 2.0 for user authorization
- Webhooks for real-time updates
- Rate limits: Vendor-specific

**Data Mapping**:
```typescript
// Apple Health → HydroTrack
{
  "HKQuantityTypeIdentifierDietaryWater": "water intake (ml)",
  "HKQuantityTypeIdentifierStepCount": "steps (count)"
}
```

**Privacy**: All data stored locally, sync opt-in only


#### AI Insights (Claude API)
**Purpose**: Generate personalized recommendations

**Endpoint**: `https://api.anthropic.com/v1/messages`
**Authentication**: API key (server-side only)
**Rate Limit**: 1000 requests/day (free tier)

**Example Request**:
```typescript
const prompt = `Based on this tracking data: ${JSON.stringify(entries)},
provide 3 actionable recommendations to improve consistency.`;

fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {
    'x-api-key': process.env.ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json'
  },
  body: JSON.stringify({
    model: 'claude-3-haiku-20240307',
    max_tokens: 500,
    messages: [{ role: 'user', content: prompt }]
  })
});
```

**Cost**: ~$0.001 per insight

---

## API Testing

### Development
```bash
# Start dev server
npm run dev

# Test healthz endpoint
curl http://localhost:3000/api/healthz

# Test auth (if backend exists)
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Automated Testing
```bash
# Unit tests (API routes)
npm run test:api

# Integration tests (full request/response)
npm run test:integration

# Load testing (optional)
npm run test:load
```

---

## API Versioning

**Strategy**: URL-based versioning

**Versions**:
- `/v1/`: Initial release (current)
- `/v2/`: Breaking changes (future)

**Deprecation Policy**:
- New version released 6 months before old deprecated
- Old version supported 12 months after deprecation
- Sunset notices in response headers

**Header**:
```
X-API-Version: 1.0.0
X-API-Deprecated: false
```

---

## References

**Standards**:
- [REST API Design](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [OAuth 2.0](https://oauth.net/2/)

**PRD Cross-References**:
- See `prd/03-acceptance-criteria.md` for API requirements
- See `architecture-data-model.md` for payload schemas
