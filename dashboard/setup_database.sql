-- ============================================
-- VEDAVATHI DASHBOARD - COMPLETE DATABASE SETUP
-- Execute this in your InsForge/Supabase SQL Editor
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. TOURISM & AGRI-TOURISM (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS tourism_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_name TEXT, guest_email TEXT, guest_phone TEXT,
    package_id TEXT, check_in DATE, check_out DATE,
    guests INTEGER, amount DECIMAL(10,2), status TEXT DEFAULT 'pending',
    notes TEXT, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tourism_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, description TEXT, price DECIMAL(10,2),
    duration_days INTEGER, includes TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tourism_guests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, email TEXT, phone TEXT, visits INTEGER DEFAULT 0,
    total_spent DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 2. CARBON CREDITS (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS carbon_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, description TEXT, area_hectares DECIMAL(10,2),
    credit_type TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS carbon_credits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id TEXT, quantity INTEGER, price_per_credit DECIMAL(10,2),
    status TEXT DEFAULT 'available', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS carbon_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credit_id TEXT, buyer_id TEXT, quantity INTEGER,
    price DECIMAL(10,2), transaction_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 3. PAINT MANUFACTURING (4 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS paint_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, code TEXT, color TEXT, finish TEXT,
    unit TEXT, cost_price DECIMAL(10,2), selling_price DECIMAL(10,2),
    stock INTEGER, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS paint_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number TEXT, customer_id TEXT, product_id TEXT,
    quantity INTEGER, amount DECIMAL(10,2), status TEXT DEFAULT 'pending',
    order_date DATE, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS paint_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id TEXT, raw_material TEXT, quantity INTEGER,
    unit TEXT, updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS paint_production (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id TEXT, batch_number TEXT, quantity INTEGER,
    produced_date DATE, status TEXT DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 4. DAIRY & CATTLE (5 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS cattle_animals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id TEXT UNIQUE, name TEXT, breed TEXT, gender TEXT,
    birth_date DATE, mother_id TEXT, father_id TEXT,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cattle_milk (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id TEXT, date DATE, shift TEXT,
    quantity_liters DECIMAL(6,2), fat_percent DECIMAL(4,2),
    snf_percent DECIMAL(4,2), rate DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cattle_health (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id TEXT, date DATE, complaint TEXT,
    diagnosis TEXT, treatment TEXT, vet_name TEXT,
    cost DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cattle_breeding (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id TEXT, breeding_date DATE, method TEXT,
    sire_id TEXT, expected_calving_date DATE,
    status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cattle_feed (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id TEXT, date DATE, feed_type TEXT,
    quantity_kg DECIMAL(6,2), cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 5. POULTRY HUB (5 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS poultry_flocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flock_name TEXT, breed TEXT, count INTEGER,
    acquisition_date DATE, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS poultry_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_number TEXT, flock_id TEXT, type TEXT,
    count INTEGER, start_date DATE, expected_end_date DATE,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS poultry_eggs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, date DATE, total_eggs INTEGER,
    broken INTEGER, sold INTEGER, rate DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS poultry_health (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, date DATE, disease TEXT,
    mortality INTEGER, treatment TEXT, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS poultry_feed (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, date DATE, feed_brand TEXT,
    quantity_kg DECIMAL(6,2), cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 6. SMART GRID (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS grid_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP DEFAULT NOW(), voltage DECIMAL(6,2),
    current_amps DECIMAL(6,2), power_kw DECIMAL(8,2),
    frequency_hz DECIMAL(5,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS grid_consumers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consumer_id TEXT UNIQUE, name TEXT, type TEXT,
    load_kw DECIMAL(8,2), location TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS grid_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_type TEXT, severity TEXT, message TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 7. SOLAR (4 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS solar_panels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    panel_id TEXT UNIQUE, location TEXT, capacity_kw DECIMAL(6,2),
    install_date DATE, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS solar_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    panel_id TEXT, timestamp TIMESTAMP,
    voltage DECIMAL(6,2), current_amps DECIMAL(6,2),
    power_kw DECIMAL(8,2), energy_kwh DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS solar_maintenance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    panel_id TEXT, date DATE, issue TEXT,
    action_taken TEXT, cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS solar_production (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE, energy_kwh DECIMAL(10,2),
    revenue DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 8. WIND (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS wind_turbines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    turbine_id TEXT UNIQUE, capacity_kw DECIMAL(8,2),
    hub_height_m DECIMAL(5,2), install_date DATE,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wind_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    turbine_id TEXT, timestamp TIMESTAMP,
    wind_speed_mps DECIMAL(5,2), power_kw DECIMAL(8,2),
    energy_kwh DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wind_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    turbine_id TEXT, alert_type TEXT, message TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 9. BIOGAS (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS biogas_plants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT UNIQUE, capacity_cubic_meters DECIMAL(8,2),
    location TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS biogas_production (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT, date DATE, gas_produced_cubic DECIMAL(8,2),
    substrate_kg DECIMAL(8,2), temperature_c DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS biogas_maintenance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT, date DATE, activity TEXT, cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 10. HYDROGEN (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS hydrogen_electrolyzers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id TEXT UNIQUE, capacity_kg_per_day DECIMAL(6,2),
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hydrogen_production (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id TEXT, date DATE, production_kg DECIMAL(6,2),
    electricity_kwh DECIMAL(10,2), efficiency_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hydrogen_storage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tank_id TEXT, capacity_kg DECIMAL(6,2),
    current_level_kg DECIMAL(6,2), pressure_bar DECIMAL(6,2),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 11. HYDROPOWER (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS hydro_plants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT UNIQUE, capacity_kw DECIMAL(10,2),
    head_meters DECIMAL(6,2), location TEXT,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hydro_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT, timestamp TIMESTAMP,
    flow_rate_cms DECIMAL(8,2), power_kw DECIMAL(10,2),
    energy_kwh DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hydro_maintenance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id TEXT, date DATE, activity TEXT, cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 12. KINETIC ENERGY (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS kinetic_floors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    floor_id TEXT UNIQUE, location TEXT,
    area_sqft INTEGER, capacity_watts INTEGER,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kinetic_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    floor_id TEXT, date DATE, energy_wh INTEGER,
    peak_power_watts INTEGER, created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 13. VERMICULTURE (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS vermi_beds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bed_number TEXT, area_sqft INTEGER, worm_count INTEGER,
    start_date DATE, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vermi_production (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bed_id TEXT, date DATE, quantity_kg DECIMAL(6,2),
    grade TEXT, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vermi_sales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quantity_kg DECIMAL(6,2), rate DECIMAL(6,2),
    amount DECIMAL(10,2), customer TEXT, sale_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 14. TREE/NURSERY (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS tree_species (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scientific_name TEXT, common_name TEXT, category TEXT,
    price_per_sapling DECIMAL(6,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tree_saplings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    species_id TEXT, quantity INTEGER, batch_number TEXT,
    sown_date DATE, ready_date DATE, status TEXT DEFAULT 'growing',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tree_sales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    species_id TEXT, quantity INTEGER, customer TEXT,
    amount DECIMAL(10,2), sale_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 15. AQUACULTURE (5 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS aqua_ponds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pond_number TEXT, area_acres DECIMAL(5,2), depth_feet DECIMAL(4,2),
    water_source TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS aqua_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pond_id TEXT, species TEXT, seed_count INTEGER,
    stock_date DATE, expected_harvest_date DATE,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS aqua_feed (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, feed_type TEXT, quantity_kg DECIMAL(6,2),
    cost DECIMAL(10,2), date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS aqua_health (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, date DATE, disease TEXT,
    symptoms TEXT, treatment TEXT, mortality INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS aqua_harvest (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id TEXT, date DATE, quantity_kg DECIMAL(10,2),
    rate DECIMAL(6,2), amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 16. VETERINARY HOSPITAL (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS vet_patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id TEXT UNIQUE, owner_name TEXT, owner_phone TEXT,
    animal_type TEXT, animal_breed TEXT, age_years INTEGER,
    gender TEXT, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vet_appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id TEXT, date DATE, time TIME,
    doctor TEXT, purpose TEXT, status TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vet_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id TEXT, date DATE, complaint TEXT,
    diagnosis TEXT, treatment TEXT, follow_up_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 17. VEDIC HUB (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS vedic_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT, description TEXT, duration_hours INTEGER,
    instructor TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vedic_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT, student_name TEXT, enrollment_date DATE,
    status TEXT DEFAULT 'enrolled', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vedic_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT, description TEXT, event_date DATE,
    venue TEXT, status TEXT DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 18. LOGISTICS (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS logistics_vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_number TEXT, type TEXT, capacity_kg DECIMAL(10,2),
    fuel_type TEXT, status TEXT DEFAULT 'available',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS logistics_trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id TEXT, driver_id TEXT, origin TEXT,
    destination TEXT, distance_km INTEGER,
    trip_date DATE, status TEXT DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS logistics_drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id TEXT UNIQUE, name TEXT, license_number TEXT,
    phone TEXT, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 19. WATER MANAGEMENT (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS water_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name TEXT, type TEXT, capacity_liters DECIMAL(12,2),
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS water_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id TEXT, timestamp TIMESTAMP, level_percentage DECIMAL(5,2),
    flow_rate_lpm DECIMAL(8,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS water_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id TEXT, consumer_type TEXT, quantity_liters DECIMAL(10,2),
    date DATE, created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 20. TRUST MANAGEMENT (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS trust_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id TEXT UNIQUE, name TEXT, phone TEXT,
    email TEXT, join_date DATE, status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trust_meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_date DATE, agenda TEXT, minutes TEXT,
    attendees TEXT, created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trust_donations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id TEXT, amount DECIMAL(10,2),
    donation_date DATE, receipt_number TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 21. COMMAND CENTER (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS command_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_type TEXT, severity TEXT, message TEXT,
    source_module TEXT, timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS command_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module TEXT, metric_name TEXT, value DECIMAL(10,2),
    unit TEXT, timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS command_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_type TEXT, description TEXT, user_id TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 22. CRM MODULE (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS crm_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, email TEXT, phone TEXT, company TEXT,
    source TEXT, status TEXT DEFAULT 'new', notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crm_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT, description TEXT, lead_id UUID,
    assigned_to TEXT, due_date DATE,
    status TEXT DEFAULT 'pending', priority TEXT DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crm_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID, type TEXT, subject TEXT,
    content TEXT, direction TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 23. HRM MODULE (4 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS hrm_employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT UNIQUE, first_name TEXT, last_name TEXT,
    email TEXT, phone TEXT, department TEXT, designation TEXT,
    join_date DATE, salary DECIMAL(10,2), status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hrm_attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT, date DATE, check_in TIME,
    check_out TIME, hours_worked DECIMAL(5,2),
    status TEXT DEFAULT 'present', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hrm_leaves (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT, leave_type TEXT, start_date DATE,
    end_date DATE, days DECIMAL(3,1), reason TEXT,
    status TEXT DEFAULT 'pending', approved_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hrm_payroll (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT, month INTEGER, year INTEGER,
    basic_salary DECIMAL(10,2), deductions DECIMAL(10,2),
    net_pay DECIMAL(10,2), payment_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 24. INVENTORY MODULE (3 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS inv_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT UNIQUE, name TEXT, category TEXT,
    unit TEXT, min_stock INTEGER, current_stock INTEGER,
    reorder_level INTEGER, cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inv_purchase_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    po_number TEXT UNIQUE, supplier_id TEXT, order_date DATE,
    expected_date DATE, total_amount DECIMAL(10,2),
    status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inv_stock_movement (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id TEXT, movement_type TEXT, quantity INTEGER,
    reference_type TEXT, reference_id TEXT, notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 25. FINANCE MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS fin_invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number TEXT UNIQUE, customer_id TEXT,
    invoice_date DATE, due_date DATE, subtotal DECIMAL(10,2),
    tax DECIMAL(10,2), total DECIMAL(10,2),
    status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fin_expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT, description TEXT, amount DECIMAL(10,2),
    date DATE, payment_mode TEXT, vendor TEXT,
    status TEXT DEFAULT 'approved', created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 26. DMS MODULE (1 table)
-- ============================================
CREATE TABLE IF NOT EXISTS dms_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT, category TEXT, file_type TEXT,
    file_path TEXT, uploaded_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 27. WORKFLOW MODULE (1 table)
-- ============================================
CREATE TABLE IF NOT EXISTS workflow_approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_type TEXT, request_id TEXT, requested_by TEXT,
    amount DECIMAL(10,2), status TEXT DEFAULT 'pending',
    approved_by TEXT, created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 28. TICKETING MODULE (1 table)
-- ============================================
CREATE TABLE IF NOT EXISTS ticketing_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_number TEXT UNIQUE, subject TEXT, description TEXT,
    priority TEXT DEFAULT 'medium', status TEXT DEFAULT 'open',
    created_by TEXT, assigned_to TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 29. BI MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS bi_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module TEXT, metric_name TEXT, value DECIMAL(10,2),
    period_start DATE, period_end DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bi_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_name TEXT, report_type TEXT, parameters JSONB,
    created_by TEXT, created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 30. BOOKING MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS bkg_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_number TEXT UNIQUE, guest_name TEXT, guest_email TEXT,
    guest_phone TEXT, booking_type TEXT, check_in DATE,
    check_out DATE, guests INTEGER, amount DECIMAL(10,2),
    status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bkg_vet_appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_number TEXT UNIQUE, owner_name TEXT, owner_phone TEXT,
    animal_type TEXT, appointment_date DATE, appointment_time TIME,
    doctor_name TEXT, status TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 31. LMS MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS lms_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT, description TEXT, category TEXT,
    modules_count INTEGER, instructor TEXT, rating DECIMAL(3,2),
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lms_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT, user_id TEXT, progress_percentage INTEGER DEFAULT 0,
    status TEXT DEFAULT 'enrolled', enrolled_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 32. FIELD SERVICE MODULE (1 table)
-- ============================================
CREATE TABLE IF NOT EXISTS fs_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_number TEXT UNIQUE, service_type TEXT, location TEXT,
    farmer_name TEXT, assigned_team TEXT, scheduled_date DATE,
    status TEXT DEFAULT 'scheduled', notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 33. FARMER PORTAL MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS fp_farmers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT UNIQUE, first_name TEXT, last_name TEXT,
    phone TEXT, village TEXT, total_acres DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fp_crops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT, crop_name TEXT, variety TEXT,
    acres DECIMAL(5,2), stage TEXT, expected_harvest DATE,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 34. SURVEY MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS sur_surveys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT, description TEXT, survey_type TEXT,
    questions_count INTEGER, status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sur_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    survey_id TEXT, respondent_name TEXT, responses JSONB,
    rating INTEGER, created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 35. SCHEMES MODULE (2 tables)
-- ============================================
CREATE TABLE IF NOT EXISTS sch_schemes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_name TEXT, department TEXT, benefit_type TEXT,
    benefit_amount DECIMAL(10,2), eligibility TEXT,
    status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sch_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT, scheme_id TEXT, application_number TEXT UNIQUE,
    applied_date DATE, status TEXT DEFAULT 'pending',
    amount DECIMAL(10,2), remarks TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
print('✅ All 95 tables created successfully!');
