# Admin Console Backend

**Design-First Software Factory**
**Version**: 1.0
**Created**: 2025-11-10

---

## Overview

This directory contains the complete backend infrastructure for the Admin Console:

- **Database schema** - PostgreSQL tables, indexes, triggers
- **Row-Level Security** - Fine-grained access control
- **Edge Functions** - Serverless API endpoints
- **Seed data** - Test data for development

---

## Directory Structure

```
supabase/
├── migrations/
│   ├── 001_core_schema.sql       # Database tables and indexes
│   └── 002_rls_policies.sql      # Row-level security policies
├── functions/
│   ├── _shared/
│   │   ├── cors.ts               # CORS utilities
│   │   └── auth.ts               # Admin verification
│   ├── admin-customers/
│   │   └── index.ts              # Customer CRUD API
│   ├── admin-projects/
│   │   └── index.ts              # Project CRUD API
│   ├── upload-design/
│   │   └── index.ts              # File upload handler
│   └── stripe-webhook/
│       └── index.ts              # Stripe event handler
├── seed.sql                       # Test data
└── README.md                      # This file
```

---

## Database Schema

### Tables

1. **customers** - Customer contact and billing info
   - Contact: name, email, phone, company
   - Billing: Stripe ID, subscription status, MRR
   - Metadata: tags, source, notes

2. **projects** - Project tracking (extends existing table)
   - Core: name, description, status
   - Product: product_type (express/concierge/website_refresh)
   - Delivery: estimated/actual dates, visual QA scores
   - Links: customer_id, design URLs

3. **project_notes** - Communication history
   - Content and author tracking
   - Visibility controls (internal vs customer-facing)
   - Attachments support

4. **invoices** - Billing and payments
   - Stripe integration (invoice ID, payment intent)
   - Line items (JSONB)
   - Status tracking (draft/sent/paid/failed/refunded)

5. **admin_users** - Admin access control
   - Role-based permissions (super_admin/admin/viewer)
   - Active/inactive status
   - Last login tracking

### Storage Buckets

- **design-uploads** - Customer design files
- **project-deliverables** - Final code and assets

---

## Edge Functions

### 1. admin-customers (`/admin-customers`)

**Methods**: GET, POST, PATCH, DELETE

**Features**:
- List customers with pagination and filtering
- Search by name, email, company
- Full CRUD operations
- Includes project counts and invoices

**Auth**: Admin only

---

### 2. admin-projects (`/admin-projects`)

**Methods**: GET, POST, PATCH, DELETE

**Features**:
- List projects with filters (status, product_type, customer)
- Full project details with customer, notes, invoices
- Support for all three product types
- Visual QA score tracking

**Auth**: Admin only

---

### 3. upload-design (`/upload-design`)

**Methods**: POST

**Features**:
- File upload to Supabase Storage
- Automatic project linking
- Access control (admin or project owner)
- Automatic URL updating on project record

**Auth**: Admin or customer (project owner)

---

### 4. stripe-webhook (`/stripe-webhook`)

**Methods**: POST

**Features**:
- Webhook signature verification
- Event handling for 8+ Stripe events
- Automatic customer/invoice sync
- Subscription status updates

**Auth**: Stripe signature

---

## Security (RLS)

### Admin Access

- Admins (super_admin, admin) have full access to all tables
- Enforced via `is_admin()` function
- RLS policies check `admin_users` table

### Customer Access

- Customers can view their own records
- Customers can view their own projects
- Customers can view customer-facing notes
- Customers can upload files to their projects

### Service Role

- Webhooks use service_role for full access
- Edge Functions use service_role for database ops
- Bypasses RLS when necessary

---

## Setup

### Prerequisites

1. Supabase CLI installed: `npm install -g supabase`
2. Docker running (for local development)

### Local Development

```bash
# Initialize Supabase
supabase init

# Start local Supabase
supabase start

# Run migrations
supabase db reset

# Load seed data
supabase db reset --seed

# Deploy Edge Functions locally
supabase functions serve
```

### Environment Variables

Create `.env`:

```bash
# Supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google OAuth (optional)
GOOGLE_CLIENT_ID=<client-id>
GOOGLE_CLIENT_SECRET=<client-secret>
```

---

## Deployment

### Deploy Database

```bash
# Link to your project
supabase link --project-ref <project-ref>

# Push migrations
supabase db push

# Seed production data (optional)
supabase db push --seed
```

### Deploy Edge Functions

```bash
# Deploy all functions
supabase functions deploy

# Deploy specific function
supabase functions deploy admin-customers

# Set environment secrets
supabase secrets set STRIPE_SECRET_KEY=sk_live_...
supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...
```

### Verify Deployment

```bash
# Test Edge Function
curl https://<project-ref>.supabase.co/functions/v1/admin-customers \
  -H "Authorization: Bearer <token>"
```

---

## Testing

### Test Credentials

**Admin Login**:
- Email: `admin@designfactory.dev`
- Password: `SupabaseShouldReset!`

**Test Data**:
- 5 customers (various statuses)
- 5 projects (various stages)
- 3 invoices (paid, sent, draft)

See [docs/admin-console/TEST_DATA.md](/design-first-software-factory/docs/admin-console/TEST_DATA.md) for full details.

### API Testing

```bash
# Get admin token
TOKEN=$(supabase auth login --email admin@designfactory.dev --password SupabaseShouldReset!)

# Test customer API
curl -H "Authorization: Bearer $TOKEN" \
  https://<project-ref>.supabase.co/functions/v1/admin-customers

# Test project API
curl -H "Authorization: Bearer $TOKEN" \
  https://<project-ref>.supabase.co/functions/v1/admin-projects
```

---

## Monitoring

### Database

```sql
-- Check table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check RLS policies
SELECT tablename, policyname, cmd, qual
FROM pg_policies
WHERE schemaname = 'public';
```

### Edge Functions

- View logs in Supabase Dashboard → Edge Functions
- Monitor invocation counts and errors
- Set up alerts for failures

---

## Documentation

- **[API Reference](../design-first-software-factory/docs/admin-console/API_REFERENCE.md)** - Complete API documentation with curl examples
- **[Test Data](../design-first-software-factory/docs/admin-console/TEST_DATA.md)** - Test credentials and sample data
- **[Google OAuth Setup](../design-first-software-factory/docs/admin-console/GOOGLE_OAUTH_SETUP.md)** - OAuth configuration guide

---

## Next Steps

1. **Frontend Development** - Build Expo/React Native admin UI
2. **OAuth Setup** - Configure Google authentication
3. **Stripe Integration** - Set up webhook endpoint
4. **Production Deployment** - Deploy to production Supabase project
5. **Monitoring Setup** - Configure alerts and logging

---

## Support

For questions or issues:
1. Review documentation in `design-first-software-factory/docs/admin-console/`
2. Check Supabase logs for errors
3. Verify RLS policies are working correctly
4. Test with seed data first before production data

---

**Backend Status**: ✅ Complete and ready for frontend integration
