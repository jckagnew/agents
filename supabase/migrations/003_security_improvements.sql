-- =====================================================
-- Security & Data Integrity Improvements
-- =====================================================
-- Created: 2025-11-12
-- Purpose: Add created_by tracking, soft deletes, improved RLS
-- =====================================================

-- =====================================================
-- 1. ADD CREATED_BY TRACKING
-- =====================================================

-- Add created_by to customers
ALTER TABLE customers ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES auth.users(id);

-- Add created_by to projects (if not exists)
ALTER TABLE projects ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES auth.users(id);

-- Add created_by to project_notes (if not exists)
ALTER TABLE project_notes ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES auth.users(id);

-- Create function to auto-set created_by
CREATE OR REPLACE FUNCTION set_created_by()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.created_by IS NULL THEN
    NEW.created_by = auth.uid();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add triggers for auto-setting created_by
CREATE TRIGGER customers_set_created_by
  BEFORE INSERT ON customers
  FOR EACH ROW
  EXECUTE FUNCTION set_created_by();

CREATE TRIGGER projects_set_created_by
  BEFORE INSERT ON projects
  FOR EACH ROW
  EXECUTE FUNCTION set_created_by();

CREATE TRIGGER project_notes_set_created_by
  BEFORE INSERT ON project_notes
  FOR EACH ROW
  EXECUTE FUNCTION set_created_by();

-- =====================================================
-- 2. ADD SOFT DELETES
-- =====================================================

-- Add deleted_at columns
ALTER TABLE customers ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE project_notes ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;

-- Add deleted_by columns
ALTER TABLE customers ADD COLUMN IF NOT EXISTS deleted_by UUID REFERENCES auth.users(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS deleted_by UUID REFERENCES auth.users(id);
ALTER TABLE project_notes ADD COLUMN IF NOT EXISTS deleted_by UUID REFERENCES auth.users(id);

-- Create indexes for soft delete queries
CREATE INDEX IF NOT EXISTS idx_customers_deleted_at ON customers(deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_projects_deleted_at ON projects(deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_project_notes_deleted_at ON project_notes(deleted_at) WHERE deleted_at IS NOT NULL;

-- Create view for non-deleted customers
CREATE OR REPLACE VIEW customers_active AS
SELECT * FROM customers WHERE deleted_at IS NULL;

-- Create view for non-deleted projects
CREATE OR REPLACE VIEW projects_active AS
SELECT * FROM projects WHERE deleted_at IS NULL;

-- =====================================================
-- 3. IMPROVED RLS POLICIES
-- =====================================================

-- Drop existing broad policies
DROP POLICY IF EXISTS "Users can view all customers" ON customers;
DROP POLICY IF EXISTS "Users can view all projects" ON projects;

-- CUSTOMERS: Users can only see their own customers
CREATE POLICY customers_select_own
  ON customers
  FOR SELECT
  TO authenticated
  USING (
    -- User is the creator
    created_by = auth.uid()
    OR
    -- User is the customer (self-service)
    user_id = auth.uid()
  );

CREATE POLICY customers_insert_own
  ON customers
  FOR INSERT
  TO authenticated
  WITH CHECK (
    created_by = auth.uid() OR created_by IS NULL
  );

CREATE POLICY customers_update_own
  ON customers
  FOR UPDATE
  TO authenticated
  USING (
    created_by = auth.uid() OR user_id = auth.uid()
  );

CREATE POLICY customers_delete_own
  ON customers
  FOR DELETE
  TO authenticated
  USING (
    created_by = auth.uid()
  );

-- PROJECTS: Users can only see projects for their customers
CREATE POLICY projects_select_own
  ON projects
  FOR SELECT
  TO authenticated
  USING (
    -- User created the project
    created_by = auth.uid()
    OR
    -- User owns the customer
    customer_id IN (
      SELECT id FROM customers WHERE created_by = auth.uid()
    )
    OR
    -- User is the customer's user
    customer_id IN (
      SELECT id FROM customers WHERE user_id = auth.uid()
    )
  );

CREATE POLICY projects_insert_own
  ON projects
  FOR INSERT
  TO authenticated
  WITH CHECK (
    created_by = auth.uid() OR created_by IS NULL
  );

CREATE POLICY projects_update_own
  ON projects
  FOR UPDATE
  TO authenticated
  USING (
    created_by = auth.uid()
    OR
    customer_id IN (
      SELECT id FROM customers WHERE created_by = auth.uid()
    )
  );

CREATE POLICY projects_delete_own
  ON projects
  FOR DELETE
  TO authenticated
  USING (
    created_by = auth.uid()
  );

-- =====================================================
-- 4. AUDIT LOGGING (Optional but recommended)
-- =====================================================

CREATE TABLE IF NOT EXISTS audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  table_name TEXT NOT NULL,
  record_id UUID NOT NULL,
  action TEXT NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
  old_data JSONB,
  new_data JSONB,
  changed_by UUID REFERENCES auth.users(id),
  changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  CONSTRAINT valid_action CHECK (action IN ('INSERT', 'UPDATE', 'DELETE', 'SOFT_DELETE'))
);

CREATE INDEX IF NOT EXISTS idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_changed_by ON audit_log(changed_by);
CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at ON audit_log(changed_at DESC);

-- Function to log changes
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    INSERT INTO audit_log (table_name, record_id, action, old_data, changed_by)
    VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD), auth.uid());
    RETURN OLD;
  ELSIF TG_OP = 'UPDATE' THEN
    -- Check if it's a soft delete
    IF NEW.deleted_at IS NOT NULL AND OLD.deleted_at IS NULL THEN
      INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
      VALUES (TG_TABLE_NAME, NEW.id, 'SOFT_DELETE', to_jsonb(OLD), to_jsonb(NEW), auth.uid());
    ELSE
      INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
      VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), auth.uid());
    END IF;
    RETURN NEW;
  ELSIF TG_OP = 'INSERT' THEN
    INSERT INTO audit_log (table_name, record_id, action, new_data, changed_by)
    VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW), auth.uid());
    RETURN NEW;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add audit triggers to important tables
CREATE TRIGGER customers_audit
  AFTER INSERT OR UPDATE OR DELETE ON customers
  FOR EACH ROW
  EXECUTE FUNCTION log_changes();

CREATE TRIGGER projects_audit
  AFTER INSERT OR UPDATE OR DELETE ON projects
  FOR EACH ROW
  EXECUTE FUNCTION log_changes();

-- =====================================================
-- 5. COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON COLUMN customers.created_by IS 'Admin user who created this customer record';
COMMENT ON COLUMN customers.deleted_at IS 'Soft delete timestamp - NULL means active';
COMMENT ON COLUMN customers.deleted_by IS 'Admin user who soft-deleted this record';

COMMENT ON COLUMN projects.created_by IS 'Admin user who created this project';
COMMENT ON COLUMN projects.deleted_at IS 'Soft delete timestamp - NULL means active';

COMMENT ON TABLE audit_log IS 'Audit trail of all changes to important tables';
COMMENT ON FUNCTION set_created_by() IS 'Automatically sets created_by to current user on INSERT';
COMMENT ON FUNCTION log_changes() IS 'Logs all changes to audit_log table';

-- =====================================================
-- NOTES:
-- =====================================================
-- 1. created_by is now automatically set via trigger
-- 2. Soft deletes allow data recovery - use UPDATE SET deleted_at = NOW() instead of DELETE
-- 3. RLS now restricts users to only their own data
-- 4. Audit log tracks all changes for compliance and debugging
-- 5. Views (customers_active, projects_active) provide easy access to non-deleted records
-- =====================================================
