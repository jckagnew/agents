-- =====================================================
-- Admin Console Core Schema
-- Design-First Software Factory
-- =====================================================
-- Created: 2025-11-10
-- Purpose: Core database schema for Admin Console MVP
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. CUSTOMERS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS customers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),

  -- Contact info
  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  company_name TEXT,

  -- Billing
  stripe_customer_id TEXT UNIQUE,
  subscription_status TEXT DEFAULT 'none',
  subscription_tier TEXT,
  mrr DECIMAL(10,2) DEFAULT 0,

  -- Status
  status TEXT DEFAULT 'active',

  -- Metadata
  notes JSONB DEFAULT '{}'::jsonb,
  tags TEXT[],
  source TEXT,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_contact_at TIMESTAMP WITH TIME ZONE,

  CONSTRAINT valid_subscription_status CHECK (subscription_status IN ('none', 'trial', 'active', 'cancelled', 'past_due')),
  CONSTRAINT valid_status CHECK (status IN ('active', 'paused', 'cancelled'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
CREATE INDEX IF NOT EXISTS idx_customers_subscription_status ON customers(subscription_status);
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at DESC);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customers_updated_at
  BEFORE UPDATE ON customers
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 2. PROJECTS TABLE EXTENSIONS
-- =====================================================

-- Add product type columns to existing projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS product_type TEXT NOT NULL DEFAULT 'express';
ALTER TABLE projects ADD COLUMN IF NOT EXISTS pricing_tier TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS estimated_delivery_date DATE;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS actual_delivery_date DATE;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS design_upload_url TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS final_code_url TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS visual_qa_score DECIMAL(5,2);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS customer_id UUID REFERENCES customers(id) ON DELETE CASCADE;

-- Add constraints
ALTER TABLE projects DROP CONSTRAINT IF EXISTS valid_product_type;
ALTER TABLE projects ADD CONSTRAINT valid_product_type CHECK (product_type IN ('express', 'concierge', 'website_refresh'));

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_projects_customer_id ON projects(customer_id);
CREATE INDEX IF NOT EXISTS idx_projects_product_type ON projects(product_type);
CREATE INDEX IF NOT EXISTS idx_projects_estimated_delivery ON projects(estimated_delivery_date);

-- =====================================================
-- 3. PROJECT NOTES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS project_notes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  author_id UUID REFERENCES auth.users(id),
  author_type TEXT NOT NULL,

  content TEXT NOT NULL,
  note_type TEXT DEFAULT 'general',
  visibility TEXT DEFAULT 'internal',

  attachments JSONB DEFAULT '[]'::jsonb,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  CONSTRAINT valid_author_type CHECK (author_type IN ('admin', 'customer')),
  CONSTRAINT valid_note_type CHECK (note_type IN ('general', 'internal', 'customer_facing')),
  CONSTRAINT valid_visibility CHECK (visibility IN ('internal', 'customer'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_project_notes_project_id ON project_notes(project_id);
CREATE INDEX IF NOT EXISTS idx_project_notes_created_at ON project_notes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_project_notes_author_id ON project_notes(author_id);

-- =====================================================
-- 4. INVOICES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS invoices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  customer_id UUID REFERENCES customers(id),
  project_id UUID REFERENCES projects(id),

  stripe_invoice_id TEXT UNIQUE,
  stripe_payment_intent_id TEXT,

  amount DECIMAL(10,2) NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'draft',

  product_type TEXT,
  line_items JSONB DEFAULT '[]'::jsonb,

  due_date DATE,
  paid_at TIMESTAMP WITH TIME ZONE,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  CONSTRAINT valid_invoice_status CHECK (status IN ('draft', 'sent', 'paid', 'failed', 'refunded')),
  CONSTRAINT valid_product_type CHECK (product_type IN ('express', 'concierge', 'website_refresh'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_project_id ON invoices(project_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_stripe_invoice_id ON invoices(stripe_invoice_id);
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON invoices(created_at DESC);

-- Updated_at trigger
CREATE TRIGGER invoices_updated_at
  BEFORE UPDATE ON invoices
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 5. ADMIN USERS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS admin_users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID UNIQUE REFERENCES auth.users(id),

  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,

  role TEXT DEFAULT 'viewer',

  permissions JSONB DEFAULT '{}'::jsonb,

  is_active BOOLEAN DEFAULT true,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login_at TIMESTAMP WITH TIME ZONE,

  CONSTRAINT valid_role CHECK (role IN ('super_admin', 'admin', 'viewer'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON admin_users(user_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);
CREATE INDEX IF NOT EXISTS idx_admin_users_role ON admin_users(role);
CREATE INDEX IF NOT EXISTS idx_admin_users_is_active ON admin_users(is_active);

-- Updated_at trigger
CREATE TRIGGER admin_users_updated_at
  BEFORE UPDATE ON admin_users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 6. STORAGE BUCKETS
-- =====================================================

-- Design uploads bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('design-uploads', 'design-uploads', false)
ON CONFLICT (id) DO NOTHING;

-- Project deliverables bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('project-deliverables', 'project-deliverables', false)
ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- 7. HELPER FUNCTIONS
-- =====================================================

-- Check if user is admin
CREATE OR REPLACE FUNCTION is_admin(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM admin_users
    WHERE user_id = user_uuid
    AND role IN ('super_admin', 'admin')
    AND is_active = true
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user is super admin
CREATE OR REPLACE FUNCTION is_super_admin(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM admin_users
    WHERE user_id = user_uuid
    AND role = 'super_admin'
    AND is_active = true
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get customer project count
CREATE OR REPLACE FUNCTION get_customer_project_count(customer_uuid UUID)
RETURNS INTEGER AS $$
BEGIN
  RETURN (
    SELECT COUNT(*)::INTEGER
    FROM projects
    WHERE customer_id = customer_uuid
  );
END;
$$ LANGUAGE plpgsql;

-- Calculate customer lifetime value
CREATE OR REPLACE FUNCTION get_customer_lifetime_value(customer_uuid UUID)
RETURNS DECIMAL AS $$
BEGIN
  RETURN (
    SELECT COALESCE(SUM(amount), 0)
    FROM invoices
    WHERE customer_id = customer_uuid
    AND status = 'paid'
  );
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SCHEMA COMPLETE
-- =====================================================
