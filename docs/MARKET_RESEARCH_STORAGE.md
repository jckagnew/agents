# Market Research Reports - Storage & Access

## 📊 Where Reports Are Stored

Market research reports are stored in **two places**:

### 1. **Supabase Database** (Primary Storage)
- **Table**: `market_research_reports`
- **Location**: Your Supabase project (`design-factory-admin`)
- **Purpose**: Persistent storage for admin console access
- **Access**: Via admin console UI or API endpoints

### 2. **GitHub Issues** (Notifications)
- **Location**: GitHub repository issues
- **Purpose**: Daily notifications and interactive updates
- **Access**: GitHub Issues tab

---

## 🗄️ Database Schema

### `market_research_reports` Table

Stores the main reports with:
- `id` - Unique report ID
- `report_date` - Date of the report (one per day)
- `executive_summary` - Quick summary
- `full_report` - Complete report text
- `market_count` - Number of markets tracked
- `market_config` - JSON snapshot of market configuration
- `created_at` / `updated_at` - Timestamps

### `market_insights` Table

Stores individual market insights:
- `report_id` - Links to main report
- `market_id` - Market identifier
- `market_name` - Market name
- `sentiment_analysis` - Market sentiment
- `key_trends` - Array of trends
- `opportunities` - Array of opportunities
- `threats` - Array of threats
- `competitor_activity` - Competitor notes
- `search_keywords` - Keywords used
- `competitors_tracked` - Competitors analyzed

---

## 🔌 API Endpoints

### Save Report (Automated)
**Endpoint**: `POST /functions/v1/save-market-research`

Called automatically by GitHub Actions workflow.

**Request Body**:
```json
{
  "report": "Full report text...",
  "marketConfig": { "markets": [...] },
  "marketInsights": [...]
}
```

### Get Reports (Admin Console)
**Endpoint**: `GET /functions/v1/get-market-research`

**Query Parameters**:
- `id` - Get specific report by ID
- `start_date` - Filter from date (YYYY-MM-DD)
- `end_date` - Filter to date (YYYY-MM-DD)
- `limit` - Max results (default: 30)

**Example**:
```
GET /functions/v1/get-market-research?start_date=2025-11-01&limit=10
```

**Response**:
```json
{
  "reports": [
    {
      "id": "uuid",
      "report_date": "2025-11-17",
      "executive_summary": "...",
      "full_report": "...",
      "market_count": 6,
      "created_at": "2025-11-17T12:00:00Z"
    }
  ]
}
```

---

## 📱 Admin Console Access

Reports can be accessed in the admin console:

1. **View All Reports**: List of all daily reports
2. **View Specific Report**: Click on a report to see full details
3. **Filter by Date**: Filter reports by date range
4. **Market Insights**: View insights by market category
5. **Search**: Full-text search across all reports

---

## 🔄 Workflow

1. **Daily at 12:00 UTC**: GitHub Actions runs research
2. **Research Script**: Generates report from 6 markets
3. **Save to Database**: Report saved via `save-market-research` function
4. **Create GitHub Issue**: Notification issue created
5. **Admin Console**: Reports available immediately for review

---

## 🔐 Security

- **RLS Enabled**: Row Level Security on all tables
- **Admin Only**: Only admin users can view reports
- **Service Role**: Automated workflows use service role key
- **CORS**: Configured for admin console domain

---

## 📈 Usage Examples

### Get Latest Report
```javascript
const response = await fetch(
  'https://your-project.supabase.co/functions/v1/get-market-research?limit=1',
  {
    headers: {
      'Authorization': `Bearer ${adminToken}`
    }
  }
);
const { reports } = await response.json();
const latestReport = reports[0];
```

### Get Reports for Date Range
```javascript
const response = await fetch(
  'https://your-project.supabase.co/functions/v1/get-market-research?start_date=2025-11-01&end_date=2025-11-17',
  {
    headers: {
      'Authorization': `Bearer ${adminToken}`
    }
  }
);
```

### View in Admin Console
Navigate to: **Admin Console > Market Research > Reports**

---

## 🚀 Next Steps

1. **Apply Migration**: Run `supabase db push` to create tables
2. **Deploy Functions**: Deploy `save-market-research` and `get-market-research`
3. **Add UI**: Create admin console UI component to display reports
4. **Test**: Run workflow manually to test database saving

---

**Status**: ✅ Database schema created  
**Status**: ✅ API endpoints created  
**Status**: ⏳ Migration needs to be applied  
**Status**: ⏳ Functions need to be deployed  
**Status**: ⏳ Admin console UI needs to be built

