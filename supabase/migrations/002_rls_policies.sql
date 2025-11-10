-- =====================================================
-- Row-Level Security Policies
-- Design-First Software Factory - Admin Console
-- =====================================================
-- Created: 2025-11-10
-- Purpose: Secure access to all tables
-- =====================================================

-- =====================================================
-- 1. ENABLE RLS ON ALL TABLES
-- =====================================================

ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 2. CUSTOMERS POLICIES
-- =====================================================

-- Admin users can do everything
CREATE POLICY customers_admin_all
  ON customers FOR ALL
  USING (is_admin(auth.uid()));

-- Customers can view their own record
CREATE POLICY customers_own_select
  ON customers FOR SELECT
  USING (user_id = auth.uid());

-- Customers can update their own profile (limited fields)
CREATE POLICY customers_own_update
  ON customers FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (
    user_id = auth.uid()
    AND full_name IS NOT NULL
    AND email IS NOT NULL
  );

-- =====================================================
-- 3. PROJECTS POLICIES
-- =====================================================

-- Admin users can do everything
CREATE POLICY projects_admin_all
  ON projects FOR ALL
  USING (is_admin(auth.uid()));

-- Customers can view their own projects
CREATE POLICY projects_customer_select
  ON projects FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM customers
      WHERE customers.id = projects.customer_id
      AND customers.user_id = auth.uid()
    )
  );

-- Service role can do everything (for webhooks)
CREATE POLICY projects_service_role_all
  ON projects FOR ALL
  USING (auth.jwt() ->> 'role' = 'service_role');

-- =====================================================
-- 4. PROJECT NOTES POLICIES
-- =====================================================

-- Admin users can do everything
CREATE POLICY project_notes_admin_all
  ON project_notes FOR ALL
  USING (is_admin(auth.uid()));

-- Customers can view customer-facing notes on their projects
CREATE POLICY project_notes_customer_select
  ON project_notes FOR SELECT
  USING (
    visibility = 'customer'
    AND EXISTS (
      SELECT 1 FROM projects
      JOIN customers ON customers.id = projects.customer_id
      WHERE projects.id = project_notes.project_id
      AND customers.user_id = auth.uid()
    )
  );

-- Customers can create notes on their own projects
CREATE POLICY project_notes_customer_insert
  ON project_notes FOR INSERT
  WITH CHECK (
    author_type = 'customer'
    AND author_id = auth.uid()
    AND EXISTS (
      SELECT 1 FROM projects
      JOIN customers ON customers.id = projects.customer_id
      WHERE projects.id = project_notes.project_id
      AND customers.user_id = auth.uid()
    )
  );

-- =====================================================
-- 5. INVOICES POLICIES
-- =====================================================

-- Admin users can do everything
CREATE POLICY invoices_admin_all
  ON invoices FOR ALL
  USING (is_admin(auth.uid()));

-- Customers can view their own invoices
CREATE POLICY invoices_customer_select
  ON invoices FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM customers
      WHERE customers.id = invoices.customer_id
      AND customers.user_id = auth.uid()
    )
  );

-- Service role can do everything (for Stripe webhooks)
CREATE POLICY invoices_service_role_all
  ON invoices FOR ALL
  USING (auth.jwt() ->> 'role' = 'service_role');

-- =====================================================
-- 6. ADMIN USERS POLICIES
-- =====================================================

-- Super admins can do everything
CREATE POLICY admin_users_super_admin_all
  ON admin_users FOR ALL
  USING (is_super_admin(auth.uid()));

-- Admin users can view all admin users
CREATE POLICY admin_users_admin_select
  ON admin_users FOR SELECT
  USING (is_admin(auth.uid()));

-- Users can view their own admin record
CREATE POLICY admin_users_own_select
  ON admin_users FOR SELECT
  USING (user_id = auth.uid());

-- Users can update their last_login_at
CREATE POLICY admin_users_own_update_login
  ON admin_users FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (
    user_id = auth.uid()
    AND (OLD.full_name = NEW.full_name)
    AND (OLD.email = NEW.email)
    AND (OLD.role = NEW.role)
  );

-- =====================================================
-- 7. STORAGE POLICIES
-- =====================================================

-- Design uploads bucket policies
CREATE POLICY design_uploads_admin_all
  ON storage.objects FOR ALL
  USING (
    bucket_id = 'design-uploads'
    AND is_admin(auth.uid())
  );

CREATE POLICY design_uploads_customer_insert
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'design-uploads'
    AND auth.uid() IS NOT NULL
  );

CREATE POLICY design_uploads_customer_select
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'design-uploads'
    AND (
      is_admin(auth.uid())
      OR (storage.foldername(name))[1] = auth.uid()::text
    )
  );

-- Project deliverables bucket policies
CREATE POLICY deliverables_admin_all
  ON storage.objects FOR ALL
  USING (
    bucket_id = 'project-deliverables'
    AND is_admin(auth.uid())
  );

CREATE POLICY deliverables_customer_select
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'project-deliverables'
    AND EXISTS (
      SELECT 1 FROM projects
      JOIN customers ON customers.id = projects.customer_id
      WHERE customers.user_id = auth.uid()
      AND (storage.foldername(name))[1] = projects.id::text
    )
  );

-- =====================================================
-- 8. SERVICE ROLE EXCEPTIONS
-- =====================================================

-- Grant service role full access (for Edge Functions)
GRANT ALL ON customers TO service_role;
GRANT ALL ON projects TO service_role;
GRANT ALL ON project_notes TO service_role;
GRANT ALL ON invoices TO service_role;
GRANT ALL ON admin_users TO service_role;

-- Grant authenticated users appropriate access
GRANT SELECT ON customers TO authenticated;
GRANT SELECT ON projects TO authenticated;
GRANT SELECT, INSERT ON project_notes TO authenticated;
GRANT SELECT ON invoices TO authenticated;
GRANT SELECT ON admin_users TO authenticated;

-- =====================================================
-- RLS POLICIES COMPLETE
-- =====================================================
