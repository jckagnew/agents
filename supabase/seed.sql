-- =====================================================
-- Seed Data for Admin Console
-- Design-First Software Factory
-- =====================================================
-- Created: 2025-11-10
-- Purpose: Test data for development
-- Note: Idempotent - safe to run multiple times
-- =====================================================

-- =====================================================
-- 1. CREATE ADMIN USER
-- =====================================================

DO $$
DECLARE
  admin_uuid UUID;
BEGIN
  -- Create auth user if not exists
  INSERT INTO auth.users (
    id,
    email,
    encrypted_password,
    email_confirmed_at,
    created_at,
    updated_at,
    raw_app_meta_data,
    raw_user_meta_data,
    is_super_admin,
    role
  ) VALUES (
    'a0000000-0000-0000-0000-000000000001'::UUID,
    'admin@designfactory.dev',
    crypt('SupabaseShouldReset!', gen_salt('bf')),
    NOW(),
    NOW(),
    NOW(),
    '{"provider": "email", "providers": ["email"]}'::jsonb,
    '{"full_name": "Admin User"}'::jsonb,
    false,
    'authenticated'
  ) ON CONFLICT (id) DO NOTHING;

  -- Create admin_users record
  INSERT INTO admin_users (
    user_id,
    full_name,
    email,
    role,
    is_active
  ) VALUES (
    'a0000000-0000-0000-0000-000000000001'::UUID,
    'Admin User',
    'admin@designfactory.dev',
    'super_admin',
    true
  ) ON CONFLICT (user_id) DO NOTHING;
END $$;

-- =====================================================
-- 2. CREATE TEST CUSTOMERS
-- =====================================================

-- Customer 1: Active Express customer
INSERT INTO customers (
  id,
  full_name,
  email,
  phone,
  company_name,
  subscription_status,
  subscription_tier,
  mrr,
  status,
  source,
  tags,
  created_at
) VALUES (
  'c0000000-0000-0000-0000-000000000001'::UUID,
  'Sarah Johnson',
  'sarah@techstartup.io',
  '+1-555-0101',
  'Tech Startup Inc',
  'active',
  'express',
  49.00,
  'active',
  'website',
  ARRAY['new-customer', 'tech'],
  NOW() - INTERVAL '30 days'
) ON CONFLICT (id) DO NOTHING;

-- Customer 2: Active Concierge customer
INSERT INTO customers (
  id,
  full_name,
  email,
  phone,
  company_name,
  subscription_status,
  subscription_tier,
  mrr,
  status,
  source,
  tags,
  created_at
) VALUES (
  'c0000000-0000-0000-0000-000000000002'::UUID,
  'Michael Chen',
  'michael@ecommerce.com',
  '+1-555-0102',
  'E-Commerce Solutions',
  'active',
  'concierge',
  299.00,
  'active',
  'referral',
  ARRAY['premium', 'e-commerce'],
  NOW() - INTERVAL '60 days'
) ON CONFLICT (id) DO NOTHING;

-- Customer 3: Trial customer
INSERT INTO customers (
  id,
  full_name,
  email,
  phone,
  company_name,
  subscription_status,
  subscription_tier,
  mrr,
  status,
  source,
  tags,
  created_at
) VALUES (
  'c0000000-0000-0000-0000-000000000003'::UUID,
  'Emily Rodriguez',
  'emily@healthapp.co',
  '+1-555-0103',
  'Health App Co',
  'trial',
  'concierge',
  0.00,
  'active',
  'agency',
  ARRAY['trial', 'health'],
  NOW() - INTERVAL '7 days'
) ON CONFLICT (id) DO NOTHING;

-- Customer 4: Past due customer
INSERT INTO customers (
  id,
  full_name,
  email,
  company_name,
  subscription_status,
  subscription_tier,
  mrr,
  status,
  source,
  tags,
  created_at
) VALUES (
  'c0000000-0000-0000-0000-000000000004'::UUID,
  'David Kim',
  'david@startup.io',
  'Startup IO',
  'past_due',
  'express',
  49.00,
  'active',
  'website',
  ARRAY['past-due', 'follow-up-needed'],
  NOW() - INTERVAL '90 days'
) ON CONFLICT (id) DO NOTHING;

-- Customer 5: Website Refresh customer
INSERT INTO customers (
  id,
  full_name,
  email,
  phone,
  company_name,
  subscription_status,
  subscription_tier,
  mrr,
  status,
  source,
  tags,
  created_at
) VALUES (
  'c0000000-0000-0000-0000-000000000005'::UUID,
  'Lisa Anderson',
  'lisa@consulting.com',
  '+1-555-0105',
  'Anderson Consulting',
  'active',
  'website_refresh',
  199.00,
  'active',
  'referral',
  ARRAY['website-refresh', 'consulting'],
  NOW() - INTERVAL '15 days'
) ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- 3. CREATE TEST PROJECTS
-- =====================================================

-- Project 1: Completed Express project
INSERT INTO projects (
  id,
  name,
  description,
  status,
  customer_id,
  product_type,
  pricing_tier,
  estimated_delivery_date,
  actual_delivery_date,
  visual_qa_score,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000001'::UUID,
  'Fitness Tracker App',
  'Mobile app for tracking workouts and nutrition',
  'COMPLETE',
  'c0000000-0000-0000-0000-000000000001'::UUID,
  'express',
  'basic',
  NOW() - INTERVAL '26 days',
  NOW() - INTERVAL '25 days',
  98.5,
  NOW() - INTERVAL '30 days'
) ON CONFLICT (id) DO NOTHING;

-- Project 2: In-progress Concierge project
INSERT INTO projects (
  id,
  name,
  description,
  status,
  customer_id,
  product_type,
  pricing_tier,
  estimated_delivery_date,
  visual_qa_score,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000002'::UUID,
  'E-Commerce Platform',
  'Full-featured online store with inventory management',
  'DEV',
  'c0000000-0000-0000-0000-000000000002'::UUID,
  'concierge',
  'premium',
  NOW() + INTERVAL '10 days',
  95.2,
  NOW() - INTERVAL '50 days'
) ON CONFLICT (id) DO NOTHING;

-- Project 3: Design phase Concierge project
INSERT INTO projects (
  id,
  name,
  description,
  status,
  customer_id,
  product_type,
  pricing_tier,
  estimated_delivery_date,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000003'::UUID,
  'Telemedicine Portal',
  'Patient portal with video consultations',
  'DESIGN',
  'c0000000-0000-0000-0000-000000000003'::UUID,
  'concierge',
  'premium',
  NOW() + INTERVAL '20 days',
  NOW() - INTERVAL '5 days'
) ON CONFLICT (id) DO NOTHING;

-- Project 4: Intake phase Express project
INSERT INTO projects (
  id,
  name,
  description,
  status,
  customer_id,
  product_type,
  estimated_delivery_date,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000004'::UUID,
  'Recipe Manager',
  'Simple app for saving and organizing recipes',
  'INTAKE',
  'c0000000-0000-0000-0000-000000000004'::UUID,
  'express',
  NOW() + INTERVAL '6 days',
  NOW() - INTERVAL '1 day'
) ON CONFLICT (id) DO NOTHING;

-- Project 5: Website Refresh in QA
INSERT INTO projects (
  id,
  name,
  description,
  status,
  customer_id,
  product_type,
  pricing_tier,
  estimated_delivery_date,
  visual_qa_score,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000005'::UUID,
  'Consulting Website Refresh',
  'Modernize existing website with new tech stack',
  'QA',
  'c0000000-0000-0000-0000-000000000005'::UUID,
  'website_refresh',
  'standard',
  NOW() + INTERVAL '3 days',
  96.8,
  NOW() - INTERVAL '12 days'
) ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- 4. CREATE PROJECT NOTES
-- =====================================================

-- Notes for Project 1
INSERT INTO project_notes (
  project_id,
  author_id,
  author_type,
  content,
  note_type,
  visibility,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000001'::UUID,
  'a0000000-0000-0000-0000-000000000001'::UUID,
  'admin',
  'Customer loved the design! Quick approval on first iteration.',
  'internal',
  'internal',
  NOW() - INTERVAL '28 days'
) ON CONFLICT DO NOTHING;

INSERT INTO project_notes (
  project_id,
  author_id,
  author_type,
  content,
  note_type,
  visibility,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000001'::UUID,
  'a0000000-0000-0000-0000-000000000001'::UUID,
  'admin',
  'Project completed and deployed. Customer very satisfied with turnaround time.',
  'customer_facing',
  'customer',
  NOW() - INTERVAL '25 days'
) ON CONFLICT DO NOTHING;

-- Notes for Project 2
INSERT INTO project_notes (
  project_id,
  author_id,
  author_type,
  content,
  note_type,
  visibility,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000002'::UUID,
  'a0000000-0000-0000-0000-000000000001'::UUID,
  'admin',
  'Customer selected Design Option B. Complex inventory requirements need special attention.',
  'internal',
  'internal',
  NOW() - INTERVAL '45 days'
) ON CONFLICT DO NOTHING;

-- Notes for Project 3
INSERT INTO project_notes (
  project_id,
  author_id,
  author_type,
  content,
  note_type,
  visibility,
  created_at
) VALUES (
  'p0000000-0000-0000-0000-000000000003'::UUID,
  'a0000000-0000-0000-0000-000000000001'::UUID,
  'admin',
  'Presenting three design options this week. Focus on HIPAA compliance in messaging.',
  'internal',
  'internal',
  NOW() - INTERVAL '3 days'
) ON CONFLICT DO NOTHING;

-- =====================================================
-- 5. CREATE INVOICES
-- =====================================================

-- Invoice for Project 1 (Paid)
INSERT INTO invoices (
  id,
  customer_id,
  project_id,
  amount,
  currency,
  status,
  product_type,
  line_items,
  paid_at,
  created_at
) VALUES (
  'i0000000-0000-0000-0000-000000000001'::UUID,
  'c0000000-0000-0000-0000-000000000001'::UUID,
  'p0000000-0000-0000-0000-000000000001'::UUID,
  49.00,
  'USD',
  'paid',
  'express',
  '[{"description": "Fitness Tracker App - Express", "amount": 49.00}]'::jsonb,
  NOW() - INTERVAL '25 days',
  NOW() - INTERVAL '30 days'
) ON CONFLICT (id) DO NOTHING;

-- Invoice for Project 2 (Sent, awaiting payment)
INSERT INTO invoices (
  id,
  customer_id,
  project_id,
  amount,
  currency,
  status,
  product_type,
  line_items,
  due_date,
  created_at
) VALUES (
  'i0000000-0000-0000-0000-000000000002'::UUID,
  'c0000000-0000-0000-0000-000000000002'::UUID,
  'p0000000-0000-0000-0000-000000000002'::UUID,
  299.00,
  'USD',
  'sent',
  'concierge',
  '[{"description": "E-Commerce Platform - Concierge Premium", "amount": 299.00}]'::jsonb,
  NOW() + INTERVAL '15 days',
  NOW() - INTERVAL '50 days'
) ON CONFLICT (id) DO NOTHING;

-- Invoice for Project 5 (Draft)
INSERT INTO invoices (
  id,
  customer_id,
  project_id,
  amount,
  currency,
  status,
  product_type,
  line_items,
  created_at
) VALUES (
  'i0000000-0000-0000-0000-000000000003'::UUID,
  'c0000000-0000-0000-0000-000000000005'::UUID,
  'p0000000-0000-0000-0000-000000000005'::UUID,
  199.00,
  'USD',
  'draft',
  'website_refresh',
  '[{"description": "Website Refresh - Standard", "amount": 199.00}]'::jsonb,
  NOW() - INTERVAL '12 days'
) ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- SEED DATA COMPLETE
-- =====================================================

-- Summary
DO $$
BEGIN
  RAISE NOTICE '==============================================';
  RAISE NOTICE 'Seed data loaded successfully!';
  RAISE NOTICE '==============================================';
  RAISE NOTICE 'Admin credentials:';
  RAISE NOTICE '  Email: admin@designfactory.dev';
  RAISE NOTICE '  Password: SupabaseShouldReset!';
  RAISE NOTICE '';
  RAISE NOTICE 'Test data created:';
  RAISE NOTICE '  - 5 customers';
  RAISE NOTICE '  - 5 projects';
  RAISE NOTICE '  - 4 project notes';
  RAISE NOTICE '  - 3 invoices';
  RAISE NOTICE '==============================================';
END $$;
