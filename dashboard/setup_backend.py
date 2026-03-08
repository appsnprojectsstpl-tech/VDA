#!/usr/bin/env python3
"""
Create Database Tables for Tier 1-3 Modules
Uses InsForge MCP to create tables
"""

# SQL to create tables for all modules
SQL_TABLES = """

-- ============================================
-- CRM MODULE TABLES
-- ============================================

-- Leads table
CREATE TABLE IF NOT EXISTS crm_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,
    email TEXT,
    phone TEXT,
    company TEXT,
    source TEXT,
    status TEXT DEFAULT 'new',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE IF NOT EXISTS crm_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT,
    description TEXT,
    lead_id UUID,
    assigned_to TEXT,
    due_date DATE,
    status TEXT DEFAULT 'pending',
    priority TEXT DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Communications table
CREATE TABLE IF NOT EXISTS crm_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID,
    type TEXT,
    subject TEXT,
    content TEXT,
    direction TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- HRM MODULE TABLES
-- ============================================

-- Employees table
CREATE TABLE IF NOT EXISTS hrm_employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    department TEXT,
    designation TEXT,
    join_date DATE,
    salary DECIMAL(10,2),
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Attendance table
CREATE TABLE IF NOT EXISTS hrm_attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT,
    date DATE,
    check_in TIME,
    check_out TIME,
    hours_worked DECIMAL(5,2),
    status TEXT DEFAULT 'present',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Leaves table
CREATE TABLE IF NOT EXISTS hrm_leaves (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT,
    leave_type TEXT,
    start_date DATE,
    end_date DATE,
    days DECIMAL(3,1),
    reason TEXT,
    status TEXT DEFAULT 'pending',
    approved_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- INVENTORY MODULE TABLES
-- ============================================

-- Products table
CREATE TABLE IF NOT EXISTS inv_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT UNIQUE,
    name TEXT,
    category TEXT,
    unit TEXT,
    min_stock INTEGER,
    current_stock INTEGER,
    reorder_level INTEGER,
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    supplier_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Purchase Orders table
CREATE TABLE IF NOT EXISTS inv_purchase_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    po_number TEXT UNIQUE,
    supplier_id TEXT,
    order_date DATE,
    expected_date DATE,
    total_amount DECIMAL(10,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Stock Movement table
CREATE TABLE IF NOT EXISTS inv_stock_movement (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id TEXT,
    movement_type TEXT,
    quantity INTEGER,
    reference_type TEXT,
    reference_id TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- FINANCE MODULE TABLES
-- ============================================

-- Invoices table
CREATE TABLE IF NOT EXISTS fin_invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number TEXT UNIQUE,
    customer_id TEXT,
    invoice_date DATE,
    due_date DATE,
    subtotal DECIMAL(10,2),
    tax DECIMAL(10,2),
    total DECIMAL(10,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Expenses table
CREATE TABLE IF NOT EXISTS fin_expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT,
    description TEXT,
    amount DECIMAL(10,2),
    date DATE,
    payment_mode TEXT,
    vendor TEXT,
    status TEXT DEFAULT 'approved',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- BOOKING MODULE TABLES
-- ============================================

-- Bookings table
CREATE TABLE IF NOT EXISTS bkg_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_number TEXT UNIQUE,
    guest_name TEXT,
    guest_email TEXT,
    guest_phone TEXT,
    booking_type TEXT,
    check_in DATE,
    check_out DATE,
    guests INTEGER,
    amount DECIMAL(10,2),
    status TEXT DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vet Appointments table
CREATE TABLE IF NOT EXISTS bkg_vet_appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_number TEXT UNIQUE,
    owner_name TEXT,
    owner_phone TEXT,
    animal_type TEXT,
    animal_breed TEXT,
    appointment_type TEXT,
    appointment_date DATE,
    appointment_time TIME,
    doctor_name TEXT,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- LMS MODULE TABLES
-- ============================================

-- Courses table
CREATE TABLE IF NOT EXISTS lms_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT,
    description TEXT,
    category TEXT,
    modules_count INTEGER,
    duration_hours INTEGER,
    instructor TEXT,
    rating DECIMAL(3,2),
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enrollments table
CREATE TABLE IF NOT EXISTS lms_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT,
    user_id TEXT,
    progress_percentage INTEGER DEFAULT 0,
    status TEXT DEFAULT 'enrolled',
    enrolled_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- ============================================
-- FIELD SERVICE MODULE TABLES
-- ============================================

-- Field Jobs table
CREATE TABLE IF NOT EXISTS fs_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_number TEXT UNIQUE,
    service_type TEXT,
    location_village TEXT,
    location_plot TEXT,
    farmer_name TEXT,
    farmer_phone TEXT,
    assigned_team TEXT,
    scheduled_date DATE,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- FARMER PORTAL TABLES
-- ============================================

-- Farmers table
CREATE TABLE IF NOT EXISTS fp_farmers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    village TEXT,
    total_acres DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Crops table
CREATE TABLE IF NOT EXISTS fp_crops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT,
    crop_name TEXT,
    variety TEXT,
    acres DECIMAL(5,2),
    stage TEXT,
    expected_harvest DATE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- SURVEY MODULE TABLES
-- ============================================

-- Surveys table
CREATE TABLE IF NOT EXISTS sur_surveys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT,
    description TEXT,
    survey_type TEXT,
    questions_count INTEGER,
    target_audience TEXT,
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Survey Responses table
CREATE TABLE IF NOT EXISTS sur_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    survey_id TEXT,
    respondent_name TEXT,
    responses JSONB,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- SCHEMES MODULE TABLES
-- ============================================

-- Schemes table
CREATE TABLE IF NOT EXISTS sch_schemes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_name TEXT,
    department TEXT,
    benefit_type TEXT,
    benefit_amount DECIMAL(10,2),
    eligibility TEXT,
    documents_needed TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Farmer Scheme Applications table
CREATE TABLE IF NOT EXISTS sch_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT,
    scheme_id TEXT,
    application_number TEXT UNIQUE,
    applied_date DATE,
    status TEXT DEFAULT 'pending',
    amount DECIMAL(10,2),
    disbursement_status TEXT,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

"""

print("SQL Tables Definition:")
print(SQL_TABLES)
print("\n--- To execute these tables, use InsForge MCP run_raw_sql function ---")
