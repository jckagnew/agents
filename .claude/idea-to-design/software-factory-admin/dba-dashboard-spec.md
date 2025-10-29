# DBA Dashboard Specification
## Software Factory Admin Dashboard

**Version**: 1.0
**Created**: 2025-10-25
**Status**: Specification Draft
**Purpose**: Modular admin dashboard for monitoring DBA (Doing Business As) entities, financial metrics, hosting costs, and analytics across Software Factory generated applications

---

## 1. Overview

### Purpose
Provide a centralized dashboard for Software Factory administrators to monitor and manage multiple DBA entities, track per-DBA financial performance, hosting costs, and user analytics.

### Key Requirements
- **Multi-DBA Support**: Surface metrics for all DBA entities in one interface
- **Financial Tracking**: Stripe revenue, hosting costs, profit margins
- **Analytics Integration**: GA4 user metrics, conversion rates, engagement
- **Scalability**: Easy addition of new DBAs without code changes
- **Security**: Role-based access control with DBA-level isolation
- **Modularity**: Pluggable data sources and metric cards

---

## 2. Data Sources

### 2.1 Financial Data

#### Stripe API
**Purpose**: Revenue tracking per DBA

**Data Points**:
- Monthly Recurring Revenue (MRR)
- One-time payments
- Subscription counts (active/churned/pending)
- Payment failures and retry status
- Customer lifetime value (LTV)
- Churn rate

**Integration**:
```javascript
// Stripe API endpoint
GET /api/admin/financials/stripe/:dbaId
{
  mrr: number,
  subscriptions: {
    active: number,
    churned: number,
    pending: number
  },
  payments: {
    total: number,
    failed: number,
    refunded: number
  },
  ltv: number
}
```

**Authentication**: Stripe secret key per DBA (stored in env variables or secrets manager)

#### Vercel Invoices API
**Purpose**: Hosting cost tracking

**Data Points**:
- Monthly hosting costs
- Bandwidth usage
- Build minutes consumed
- Serverless function invocations
- Team member count (for team plans)

**Integration**:
```javascript
// Vercel API endpoint
GET /api/admin/hosting/vercel/:dbaId
{
  monthlyCost: number,
  bandwidth: { used: number, limit: number },
  buildMinutes: { used: number, limit: number },
  functionInvocations: number,
  teamMembers: number
}
```

**Authentication**: Vercel API token per DBA

### 2.2 Analytics Data

#### Google Analytics 4 (GA4)
**Purpose**: User behavior and engagement metrics

**Data Points**:
- Active users (daily/weekly/monthly)
- Session duration
- Bounce rate
- Top pages/screens
- Conversion events (sign-ups, purchases, feature usage)
- Traffic sources (organic, paid, referral)
- User demographics (if enabled)

**Integration**:
```javascript
// GA4 API endpoint
GET /api/admin/analytics/ga4/:dbaId
{
  activeUsers: {
    daily: number,
    weekly: number,
    monthly: number
  },
  engagement: {
    avgSessionDuration: number,
    bounceRate: number,
    pageViewsPerSession: number
  },
  conversions: {
    signups: number,
    purchases: number,
    customEvents: object
  },
  traffic: {
    organic: number,
    paid: number,
    referral: number,
    direct: number
  }
}
```

**Authentication**: GA4 service account credentials per DBA

### 2.3 Application Metadata

#### DBA Registry
**Purpose**: Centralized DBA configuration and metadata

**Data Structure**:
```json
{
  "dbas": [
    {
      "id": "clevel-sales-guy",
      "name": "C-Level Sales Guy",
      "domain": "clevelsalesguy.com",
      "status": "active",
      "createdAt": "2024-01-15",
      "integrations": {
        "stripe": {
          "accountId": "acct_xxx",
          "enabled": true
        },
        "vercel": {
          "teamId": "team_xxx",
          "enabled": true
        },
        "ga4": {
          "propertyId": "123456789",
          "enabled": true
        }
      },
      "tags": ["saas", "b2b", "sales"],
      "owner": "jack@example.com"
    }
  ]
}
```

**Storage**: `.claude/idea-to-design/global/dba-registry.json`

---

## 3. UI Layout

### 3.1 Dashboard Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Software Factory Admin                    [User] [Logout]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Filters:                                                     │
│  [All DBAs ▼] [Date Range: Last 30 Days ▼] [Export ⬇]       │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  Overview KPI Cards                                          │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐│
│  │ Total MRR    │ Total Users  │ Hosting Cost │ Margin     ││
│  │ $12,500      │ 1,247        │ $450         │ 96.4%      ││
│  │ +8.5% ↑      │ +12.3% ↑     │ +2.1% ↑      │ +0.5% ↑    ││
│  └──────────────┴──────────────┴──────────────┴────────────┘│
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  Per-DBA Breakdown                                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ C-Level Sales Guy                    [View Details →]   ││
│  │ MRR: $8,200  | Users: 892  | Hosting: $250  | 97% ↑     ││
│  │ ████████████████████████░░░░░░░░░ Revenue Trend          ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Weight Tracker App                   [View Details →]   ││
│  │ MRR: $2,800  | Users: 245  | Hosting: $120  | 95.7% ↑   ││
│  │ ██████████████░░░░░░░░░░░░░░ Revenue Trend              ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Job Search Assistant                 [View Details →]   ││
│  │ MRR: $1,500  | Users: 110  | Hosting: $80   | 94.7% ↑   ││
│  │ ███████░░░░░░░░░░░░░░░░░░░░░ Revenue Trend              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 DBA Detail View

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard        C-Level Sales Guy                │
├─────────────────────────────────────────────────────────────┤
│  Financial Metrics                                           │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐│
│  │ MRR          │ Active Subs  │ Churn Rate   │ LTV        ││
│  │ $8,200       │ 164          │ 2.3%         │ $1,450     ││
│  └──────────────┴──────────────┴──────────────┴────────────┘│
│                                                               │
│  Revenue Trend (Last 6 Months)                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ $10k ┤                                            ●       ││
│  │  $8k ┤                                    ●       │       ││
│  │  $6k ┤                            ●       │       │       ││
│  │  $4k ┤                    ●       │       │       │       ││
│  │  $2k ┤            ●       │       │       │       │       ││
│  │   $0 └────────────────────────────────────────────────   ││
│  │       May    Jun    Jul    Aug    Sep    Oct             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Hosting Metrics                                             │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Cost         │ Bandwidth    │ Function Calls           │ │
│  │ $250/mo      │ 45GB / 100GB │ 1.2M / 2M                │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
│                                                               │
│  Analytics Metrics                                           │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐│
│  │ DAU          │ WAU          │ MAU          │ Bounce     ││
│  │ 89           │ 342          │ 892          │ 28%        ││
│  └──────────────┴──────────────┴──────────────┴────────────┘│
│                                                               │
│  Top Pages (This Month)                                      │
│  1. /dashboard - 12,345 views                                │
│  2. /partners - 3,456 views                                  │
│  3. /pricing - 2,890 views                                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Component Hierarchy

```
<DBADashboard>
  <Header>
    <Logo />
    <UserMenu />
  </Header>

  <Filters>
    <DBASelector onChange={handleDBAFilter} />
    <DateRangePicker onChange={handleDateFilter} />
    <ExportButton onClick={handleExport} />
  </Filters>

  <OverviewKPIs>
    <KPICard label="Total MRR" value={totalMRR} trend={trendMRR} />
    <KPICard label="Total Users" value={totalUsers} trend={trendUsers} />
    <KPICard label="Hosting Cost" value={hostingCost} trend={trendCost} />
    <KPICard label="Margin" value={margin} trend={trendMargin} />
  </OverviewKPIs>

  <DBAList>
    {dbas.map(dba => (
      <DBACard key={dba.id} dba={dba}>
        <MetricRow label="MRR" value={dba.mrr} />
        <MetricRow label="Users" value={dba.users} />
        <MetricRow label="Hosting" value={dba.hosting} />
        <MetricRow label="Margin" value={dba.margin} />
        <MiniChart data={dba.revenueHistory} />
        <Link to={`/dba/${dba.id}`}>View Details →</Link>
      </DBACard>
    ))}
  </DBAList>
</DBADashboard>
```

---

## 4. Security & Access Control

### 4.1 Authentication

**Method**: OAuth 2.0 with Google Workspace SSO

**Flow**:
1. User visits `/admin`
2. Redirect to Google OAuth consent screen
3. Validate email against allowed domain (`@clevelsalesguy.com`)
4. Create JWT session token (expires 24 hours)
5. Store session in HTTP-only cookie

**Implementation**:
```javascript
// Next.js middleware
export async function middleware(req) {
  const token = req.cookies.get('admin_session');

  if (!token) {
    return NextResponse.redirect('/admin/login');
  }

  const session = await verifyJWT(token);
  if (!session || !isAuthorizedEmail(session.email)) {
    return NextResponse.redirect('/admin/unauthorized');
  }

  return NextResponse.next();
}
```

### 4.2 Authorization

**Role-Based Access Control (RBAC)**:

| Role | Access | Notes |
|------|--------|-------|
| **Super Admin** | All DBAs, all data, export, delete | Owner/founder only |
| **Finance Admin** | All DBAs, financial data only | Finance team |
| **Analytics Admin** | All DBAs, analytics data only | Product/growth team |
| **DBA Owner** | Single DBA, all data | Per-DBA permission |
| **Read-Only** | All DBAs, view only (no export) | External consultants |

**Implementation**:
```javascript
// User permissions stored in database
{
  "email": "jack@clevelsalesguy.com",
  "role": "super_admin",
  "dbaAccess": ["*"],
  "permissions": ["read", "write", "export", "delete"]
}

// Middleware check
function checkPermission(user, action, dbaId) {
  if (user.role === 'super_admin') return true;

  if (!user.dbaAccess.includes('*') && !user.dbaAccess.includes(dbaId)) {
    return false;
  }

  return user.permissions.includes(action);
}
```

### 4.3 Data Isolation

**Per-DBA API Keys**:
- Stripe API keys stored per DBA in environment variables
- Vercel API tokens scoped to team
- GA4 service accounts with property-level access
- No cross-DBA data leakage

**Database Structure**:
```sql
-- Separate tables per DBA
CREATE TABLE clevel_sales_guy_metrics (
  date DATE PRIMARY KEY,
  mrr DECIMAL(10,2),
  users INT,
  hosting_cost DECIMAL(10,2)
);

CREATE TABLE weight_tracker_metrics (
  date DATE PRIMARY KEY,
  mrr DECIMAL(10,2),
  users INT,
  hosting_cost DECIMAL(10,2)
);

-- OR use multi-tenant with DBA ID
CREATE TABLE dba_metrics (
  dba_id VARCHAR(50),
  date DATE,
  mrr DECIMAL(10,2),
  users INT,
  hosting_cost DECIMAL(10,2),
  PRIMARY KEY (dba_id, date)
);
```

### 4.4 Audit Logging

**Track all admin actions**:
```javascript
{
  "timestamp": "2025-10-25T14:30:00Z",
  "user": "jack@clevelsalesguy.com",
  "action": "view_financial_data",
  "dbaId": "clevel-sales-guy",
  "ipAddress": "192.168.1.100",
  "userAgent": "Mozilla/5.0...",
  "success": true
}
```

**Logged Actions**:
- Login/logout
- View DBA details
- Export data
- Modify DBA settings
- API key rotations

---

## 5. Extensibility

### 5.1 Adding New DBAs

**Zero-Code Approach**:

1. **Update DBA Registry**:
```json
// .claude/idea-to-design/global/dba-registry.json
{
  "dbas": [
    {
      "id": "new-app-name",
      "name": "New App Name",
      "domain": "newapp.com",
      "status": "active",
      "createdAt": "2025-11-01",
      "integrations": {
        "stripe": {
          "accountId": "acct_NEW123",
          "enabled": true
        },
        "vercel": {
          "teamId": "team_NEW123",
          "enabled": true
        },
        "ga4": {
          "propertyId": "987654321",
          "enabled": true
        }
      },
      "tags": ["new-category"],
      "owner": "owner@example.com"
    }
  ]
}
```

2. **Add Environment Variables**:
```bash
# .env
STRIPE_SECRET_KEY_NEW_APP=sk_live_xxx
VERCEL_API_TOKEN_NEW_APP=xxx
GA4_SERVICE_ACCOUNT_NEW_APP=xxx
```

3. **Dashboard Auto-Discovery**:
Dashboard automatically reads `dba-registry.json` and displays new DBA without code changes.

### 5.2 Adding New Metrics

**Plugin Architecture**:

```javascript
// plugins/custom-metric.js
export default {
  id: 'custom-conversion-rate',
  name: 'Custom Conversion Rate',
  category: 'analytics',

  async fetchData(dbaId, dateRange) {
    // Custom data fetching logic
    const data = await fetchCustomData(dbaId, dateRange);
    return {
      value: data.conversionRate,
      trend: data.trend,
      sparkline: data.history
    };
  },

  render(data) {
    return (
      <KPICard
        label="Custom Conversion"
        value={`${data.value}%`}
        trend={data.trend}
      />
    );
  }
};
```

**Plugin Registration**:
```javascript
// dashboard-config.js
import customConversionRate from './plugins/custom-metric';

export const metricPlugins = [
  customConversionRate,
  // ... other plugins
];
```

### 5.3 Custom Integrations

**Integration Interface**:
```typescript
interface Integration {
  id: string;
  name: string;
  auth: {
    type: 'api_key' | 'oauth' | 'service_account';
    setup(): Promise<void>;
  };
  fetchData(dbaId: string, params: object): Promise<any>;
  transform(rawData: any): MetricData;
}
```

**Example: Plausible Analytics Integration**:
```javascript
export const plausibleIntegration = {
  id: 'plausible',
  name: 'Plausible Analytics',

  auth: {
    type: 'api_key',
    async setup() {
      return process.env.PLAUSIBLE_API_KEY;
    }
  },

  async fetchData(dbaId, { startDate, endDate }) {
    const response = await fetch(
      `https://plausible.io/api/v1/stats/aggregate?site_id=${dbaId}&period=custom&date=${startDate},${endDate}`,
      { headers: { Authorization: `Bearer ${await this.auth.setup()}` } }
    );
    return response.json();
  },

  transform(rawData) {
    return {
      visitors: rawData.visitors.value,
      pageviews: rawData.pageviews.value,
      bounceRate: rawData.bounce_rate.value
    };
  }
};
```

---

## 6. Technical Architecture

### 6.1 Tech Stack

**Frontend**:
- **Framework**: Next.js 14 (App Router)
- **UI Library**: Shadcn UI + Tailwind CSS
- **Charts**: Recharts or Chart.js
- **State Management**: React Context + SWR for data fetching
- **Auth**: NextAuth.js

**Backend**:
- **API**: Next.js API Routes (serverless functions)
- **Database**: PostgreSQL (for metric storage and aggregation)
- **Caching**: Redis (for API response caching)
- **Job Queue**: BullMQ (for scheduled data sync)

**Deployment**:
- **Platform**: Vercel
- **Database**: Supabase or Railway
- **Monitoring**: Sentry for errors, Uptime Robot for availability

### 6.2 Data Flow

```
┌─────────────┐
│ External    │
│ APIs        │
│ (Stripe,    │
│  Vercel,    │
│  GA4)       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Sync Jobs   │
│ (Cron/Queue)│
│ Hourly/     │
│ Daily       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │
│ (Aggregated │
│  Metrics)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Routes  │
│ (Next.js)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Dashboard   │
│ UI (React)  │
└─────────────┘
```

### 6.3 Database Schema

```sql
-- DBA registry
CREATE TABLE dbas (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  domain VARCHAR(255),
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB
);

-- Daily metrics rollup
CREATE TABLE daily_metrics (
  id SERIAL PRIMARY KEY,
  dba_id VARCHAR(50) REFERENCES dbas(id),
  date DATE NOT NULL,
  mrr DECIMAL(10,2),
  active_subscriptions INT,
  churned_subscriptions INT,
  hosting_cost DECIMAL(10,2),
  active_users INT,
  new_users INT,
  bounce_rate DECIMAL(5,2),
  avg_session_duration INT,
  raw_data JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(dba_id, date)
);

-- User access control
CREATE TABLE admin_users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(50) NOT NULL,
  dba_access TEXT[], -- Array of DBA IDs or ['*'] for all
  permissions TEXT[], -- ['read', 'write', 'export', 'delete']
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP
);

-- Audit log
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  user_email VARCHAR(255),
  action VARCHAR(100),
  dba_id VARCHAR(50),
  ip_address INET,
  user_agent TEXT,
  success BOOLEAN,
  timestamp TIMESTAMP DEFAULT NOW()
);
```

### 6.4 API Endpoints

```
GET  /api/admin/dbas                    # List all DBAs
GET  /api/admin/dbas/:id                # Get DBA details
GET  /api/admin/metrics/overview        # Aggregated metrics across all DBAs
GET  /api/admin/metrics/:dbaId          # Metrics for specific DBA
GET  /api/admin/financials/:dbaId       # Financial data (Stripe)
GET  /api/admin/hosting/:dbaId          # Hosting metrics (Vercel)
GET  /api/admin/analytics/:dbaId        # Analytics data (GA4)
POST /api/admin/export                  # Export data to CSV/Excel
GET  /api/admin/audit-logs              # View audit logs
POST /api/admin/sync/:dbaId             # Trigger manual data sync
```

---

## 7. Development Roadmap

### Phase 1: MVP (4-6 weeks)
- [ ] Basic dashboard UI with hardcoded data
- [ ] DBA registry and configuration
- [ ] Google OAuth authentication
- [ ] Stripe integration for 1-2 DBAs
- [ ] Basic KPI cards (MRR, users, hosting cost)
- [ ] PostgreSQL database setup
- [ ] Simple DBA detail view

### Phase 2: Integration (3-4 weeks)
- [ ] Vercel API integration
- [ ] GA4 API integration
- [ ] Automated data sync jobs (hourly)
- [ ] Historical data storage and charting
- [ ] Export functionality (CSV)
- [ ] Role-based access control
- [ ] Audit logging

### Phase 3: Polish (2-3 weeks)
- [ ] Advanced filtering and search
- [ ] Custom date range selection
- [ ] Mobile responsive design
- [ ] Performance optimization
- [ ] Error handling and retry logic
- [ ] Documentation for adding new DBAs

### Phase 4: Enhancement (Ongoing)
- [ ] Plugin architecture for custom metrics
- [ ] Real-time notifications (Slack/email)
- [ ] Budget alerts and anomaly detection
- [ ] Multi-DBA comparison view
- [ ] White-label provisioning wizard (see parking lot)
- [ ] Automated partner billing exports (see parking lot)

---

## 8. Success Metrics

### Operational Efficiency
- Time to add new DBA: < 15 minutes
- Time to generate financial report: < 5 seconds
- Dashboard page load time: < 2 seconds

### Data Accuracy
- Metric freshness: < 1 hour lag
- Data sync success rate: > 99%
- API error rate: < 0.5%

### User Adoption
- Admin logins per week: > 3x (at least weekly review)
- Export usage: > 10 exports/month
- Average session time: > 5 minutes (indicates useful exploration)

---

## 9. Open Questions

1. **Real-time vs Batch Updates**: Should metrics update in real-time or via scheduled batch jobs? (Recommendation: Batch for cost efficiency)

2. **Multi-Currency Support**: Do DBAs operate in different currencies? Need Stripe currency conversion?

3. **Historical Data Retention**: How long should we store daily metrics? (Recommendation: 2 years online, archive to S3 after)

4. **Custom Alerts**: Should dashboard send notifications for anomalies (e.g., sudden MRR drop)? (Nice-to-have for Phase 4)

5. **White-Label Branding**: Will each DBA need its own branded admin dashboard, or is a single shared dashboard sufficient? (Current spec assumes shared)

---

## 10. Related Documentation

- **Backlog Items**: `.claude/idea-to-design/global/backlog/manual-queue.json`
  - "Design DBA metrics view for Software Factory admin" (P2)
  - "Implement API endpoints to serve per-DBA analytics" (P2)

- **Parking Lot Ideas**: `.claude/idea-to-design/global/parking/`
  - "Automated partner billing exports" (Future enhancement)
  - "White-label provisioning wizard" (Future enhancement)

- **DBA Registry**: `.claude/idea-to-design/global/dba-registry.json`

---

**Version History**:
- v1.0 (2025-10-25): Initial specification draft

**Next Steps**:
1. Review spec with stakeholders
2. Create backlog items for MVP development
3. Set up development environment (Next.js + Supabase)
4. Start with Phase 1 (hardcoded data prototype)
