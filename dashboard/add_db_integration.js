// ============================================
// COMPLETE DATABASE INTEGRATION LAYER
// For ALL 36 Vedavathi Dashboard Modules
// ============================================

try {

    // Helper function for error handling
    async function withErrorHandling(promise, fallback = []) {
        try {
            const data = await promise;
            return { data, error: null };
        } catch (error) {
            console.error('Database error:', error);
            return { data: fallback, error: error.message };
        }
    }

    // ============================================
    // 1. TOURISM & AGRI-TOURISM MODULE
    // ============================================
    window.dbTourism = {
        async getBookings(status, date) {
            const { data } = await withErrorHandling(window.insforge.fetch('tourism_bookings'));
            return { data };
        },
        async createBooking(booking) {
            return await withErrorHandling(window.insforge.insert('tourism_bookings', {
                ...booking,
                created_at: new Date().toISOString()
            }));
        },
        async getPackages() {
            return await withErrorHandling(window.insforge.fetch('tourism_packages'));
        },
        async getGuests() {
            return await withErrorHandling(window.insforge.fetch('tourism_guests'));
        }
    };

    // ============================================
    // 2. CARBON CREDITS MODULE
    // ============================================
    window.dbCarbon = {
        async getProjects() {
            return await withErrorHandling(window.insforge.fetch('carbon_projects'));
        },
        async createProject(project) {
            return await withErrorHandling(window.insforge.insert('carbon_projects', project));
        },
        async getCredits() {
            return await withErrorHandling(window.insforge.fetch('carbon_credits'));
        },
        async getTransactions() {
            return await withErrorHandling(window.insforge.fetch('carbon_transactions'));
        }
    };

    // ============================================
    // 3. PAINT MANUFACTURING MODULE
    // ============================================
    window.dbPaint = {
        async getProducts() {
            return await withErrorHandling(window.insforge.fetch('paint_products'));
        },
        async createProduct(product) {
            return await withErrorHandling(window.insforge.insert('paint_products', product));
        },
        async getOrders() {
            return await withErrorHandling(window.insforge.fetch('paint_orders'));
        },
        async getInventory() {
            return await withErrorHandling(window.insforge.fetch('paint_inventory'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('paint_production'));
        }
    };

    // ============================================
    // 4. POULTRY HUB MODULE
    // ============================================
    window.dbPoultry = {
        // Flock Management
        async getFlocks() {
            return await withErrorHandling(window.insforge.fetch('poultry_flocks'));
        },
        async addFlock(flock) {
            return await withErrorHandling(window.insforge.insert('poultry_flocks', flock));
        },
        // Batch Management
        async getBatches() {
            return await withErrorHandling(window.insforge.fetch('poultry_batches'));
        },
        async addBatch(batch) {
            return await withErrorHandling(window.insforge.insert('poultry_batches', batch));
        },
        // Egg Management
        async getEggs() {
            return await withErrorHandling(window.insforge.fetch('poultry_eggs'));
        },
        async recordEggs(eggs) {
            return await withErrorHandling(window.insforge.insert('poultry_eggs', eggs));
        },
        // Broiler Management
        async getBroilers() {
            return await withErrorHandling(window.insforge.fetch('poultry_broilers'));
        },
        // Health Records
        async getHealthRecords() {
            return await withErrorHandling(window.insforge.fetch('poultry_health'));
        },
        async addHealthRecord(record) {
            return await withErrorHandling(window.insforge.insert('poultry_health', record));
        },
        // Feed Management
        async getFeedInventory() {
            return await withErrorHandling(window.insforge.fetch('poultry_feed'));
        },
        // Financial
        async getExpenses() {
            return await withErrorHandling(window.insforge.fetch('poultry_expenses'));
        },
        async getRevenue() {
            return await withErrorHandling(window.insforge.fetch('poultry_revenue'));
        },
        // Advanced Analytics
        async getFCR(batchId) {
            const { data: feed } = await withErrorHandling(window.insforge.fetch('poultry_feed'));
            const { data: batches } = await withErrorHandling(window.insforge.fetch('poultry_batches'));

            const batch = batches?.find(b => b.id === batchId);
            if (!batch) return { data: null };

            const totalFeed = feed?.filter(f => f.batch_id === batchId)
                .reduce((sum, f) => sum + (parseFloat(f.quantity_kg) || 0), 0) || 0;
            const currentWeight = batch.current_weight || 0;
            const fcr = currentWeight > 0 ? (totalFeed / currentWeight).toFixed(2) : 0;

            return { data: { feedConsumed: totalFeed.toFixed(2), currentWeight, fcr } };
        },
        async getEggProductionStats(month, year) {
            const { data } = await withErrorHandling(window.insforge.fetch('poultry_eggs'));
            const filtered = data?.filter(e => {
                const d = new Date(e.date);
                return d.getMonth() + 1 === month && d.getFullYear() === year;
            }) || [];

            const totalEggs = filtered.reduce((sum, e) => sum + (e.total_eggs || 0), 0);
            const broken = filtered.reduce((sum, e) => sum + (e.broken || 0), 0);
            const sold = filtered.reduce((sum, e) => sum + (e.sold || 0), 0);
            const revenue = filtered.reduce((sum, e) => sum + ((e.sold || 0) * (parseFloat(e.rate) || 0)), 0);

            return { data: { totalEggs, broken, sold, damaged: broken + (totalEggs - broken - sold), revenue: revenue.toFixed(2) } };
        },
        async getMortalityAnalysis(month, year) {
            const { data } = await withErrorHandling(window.insforge.fetch('poultry_health'));
            const filtered = data?.filter(h => {
                const d = new Date(h.date);
                return d.getMonth() + 1 === month && d.getFullYear() === year && h.mortality > 0;
            }) || [];

            const totalMortality = filtered.reduce((sum, h) => sum + (h.mortality || 0), 0);
            const byDisease = {};
            filtered.forEach(h => {
                byDisease[h.disease || 'Unknown'] = (byDisease[h.disease || 'Unknown'] || 0) + h.mortality;
            });

            return { data: { totalMortality, byDisease } };
        }
    };

    // ============================================
    // 5. CRM & CONTRACTS MODULE
    // ============================================
    window.dbCRM = {
        async getLeads() {
            return await withErrorHandling(window.insforge.fetch('crm_leads'));
        },
        async addLead(lead) {
            return await withErrorHandling(window.insforge.insert('crm_leads', {
                ...lead,
                created_at: new Date().toISOString()
            }));
        },
        async getTasks() {
            return await withErrorHandling(window.insforge.fetch('crm_tasks'));
        },
        async getCommunications(leadId) {
            const { data } = await withErrorHandling(window.insforge.fetch('crm_communications'));
            return { data: leadId ? data?.filter(c => c.lead_id === leadId) : data };
        },
        async getContracts() {
            return await withErrorHandling(window.insforge.fetch('crm_contracts'));
        },
        async createContract(contract) {
            return await withErrorHandling(window.insforge.insert('crm_contracts', contract));
        },
        // Advanced CRM Functions
        async getLeadAnalytics() {
            const { data } = await withErrorHandling(window.insforge.fetch('crm_leads'));
            const byStatus = {};
            const bySource = {};
            data?.forEach(l => {
                byStatus[l.status] = (byStatus[l.status] || 0) + 1;
                bySource[l.source] = (bySource[l.source] || 0) + 1;
            });
            return { data: { byStatus, bySource, total: data?.length || 0 } };
        },
        async getSalesPipeline() {
            const { data: leads } = await withErrorHandling(window.insforge.fetch('crm_leads'));
            const { data: contracts } = await withErrorHandling(window.insforge.fetch('crm_contracts'));

            const newLeads = leads?.filter(l => l.status === 'new').length || 0;
            const qualified = leads?.filter(l => l.status === 'qualified').length || 0;
            const proposal = leads?.filter(l => l.status === 'proposal').length || 0;
            const won = contracts?.filter(c => c.status === 'active').length || 0;

            return { data: { new: newLeads, qualified, proposal, won, conversionRate: leads?.length ? (won / leads.length * 100).toFixed(1) : 0 } };
        },
        async getTaskSummary() {
            const { data } = await withErrorHandling(window.insforge.fetch('crm_tasks'));
            const pending = data?.filter(t => t.status === 'pending').length || 0;
            const completed = data?.filter(t => t.status === 'completed').length || 0;
            const overdue = data?.filter(t => new Date(t.due_date) < new Date() && t.status === 'pending').length || 0;

            return { data: { pending, completed, overdue, completionRate: data?.length ? (completed / data.length * 100).toFixed(1) : 0 } };
        }
    };

    // ============================================
    // 6. SMART GRID MODULE
    // ============================================
    window.dbGrid = {
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('grid_readings'));
        },
        async addReading(reading) {
            return await withErrorHandling(window.insforge.insert('grid_readings', reading));
        },
        async getAlerts() {
            return await withErrorHandling(window.insforge.fetch('grid_alerts'));
        },
        async getConsumption() {
            return await withErrorHandling(window.insforge.fetch('grid_consumption'));
        }
    };

    // ============================================
    // 7. SOLAR ENERGY MODULE
    // ============================================
    window.dbSolar = {
        async getPanels() {
            return await withErrorHandling(window.insforge.fetch('solar_panels'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('solar_readings'));
        },
        async addReading(reading) {
            return await withErrorHandling(window.insforge.insert('solar_readings', reading));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('solar_production'));
        },
        // Advanced Analytics
        async getEnergyStats(startDate, endDate) {
            const { data } = await withErrorHandling(window.insforge.fetch('solar_readings'));
            const filtered = data?.filter(r => {
                const d = new Date(r.timestamp);
                return d >= new Date(startDate) && d <= new Date(endDate);
            }) || [];

            const totalEnergy = filtered.reduce((sum, r) => sum + (parseFloat(r.energy_kwh) || 0), 0);
            const avgPower = filtered.length ? filtered.reduce((s, r) => s + (parseFloat(r.power_kw) || 0), 0) / filtered.length : 0;

            return { data: { totalEnergy: totalEnergy.toFixed(2), avgPower: avgPower.toFixed(2), readings: filtered.length } };
        },
        async getEfficiency() {
            const { data: panels } = await withErrorHandling(window.insforge.fetch('solar_panels'));
            const { data: readings } = await withErrorHandling(window.insforge.fetch('solar_readings'));

            const totalCapacity = panels?.reduce((sum, p) => sum + (parseFloat(p.capacity_kw) || 0), 0) || 0;
            const latestReadings = readings?.slice(-24) || [];
            const avgOutput = latestReadings.length ? latestReadings.reduce((s, r) => s + (parseFloat(r.power_kw) || 0), 0) / latestReadings.length : 0;
            const efficiency = totalCapacity > 0 ? (avgOutput / totalCapacity * 100).toFixed(1) : 0;

            return { data: { capacity: totalCapacity, output: avgOutput.toFixed(2), efficiency } };
        },
        async forecastNextDay() {
            const { data } = await withErrorHandling(window.insforge.fetch('solar_production'));
            const recent = data?.slice(-7) || [];
            const avgDaily = recent.length ? recent.reduce((s, r) => s + (parseFloat(r.energy_kwh) || 0), 0) / recent.length : 0;

            return { data: { forecast: avgDaily.toFixed(2), confidence: recent.length >= 5 ? 'High' : 'Low' } };
        }
    };

    // ============================================
    // 8. WIND ENERGY MODULE
    // ============================================
    window.dbWind = {
        async getTurbines() {
            return await withErrorHandling(window.insforge.fetch('wind_turbines'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('wind_readings'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('wind_production'));
        }
    };

    // ============================================
    // 9. BIOGAS MODULE
    // ============================================
    window.dbBiogas = {
        async getPlants() {
            return await withErrorHandling(window.insforge.fetch('biogas_plants'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('biogas_readings'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('biogas_production'));
        }
    };

    // ============================================
    // 10. HYDROGEN POWER MODULE
    // ============================================
    window.dbHydrogen = {
        async getElectrolyzers() {
            return await withErrorHandling(window.insforge.fetch('hydrogen_electrolyzers'));
        },
        async getStorage() {
            return await withErrorHandling(window.insforge.fetch('hydrogen_storage'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('hydrogen_production'));
        }
    };

    // ============================================
    // 11. HYDROPOWER MODULE
    // ============================================
    window.dbHydro = {
        async getTurbines() {
            return await withErrorHandling(window.insforge.fetch('hydro_turbines'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('hydro_readings'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('hydro_production'));
        }
    };

    // ============================================
    // 12. KINETIC ENERGY MODULE
    // ============================================
    window.dbKinetic = {
        async getDevices() {
            return await withErrorHandling(window.insforge.fetch('kinetic_devices'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('kinetic_readings'));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('kinetic_production'));
        }
    };

    // ============================================
    // 13. CATTLE & DAIRY MODULE
    // ============================================
    window.dbCattle = {
        async getAnimals() {
            return await withErrorHandling(window.insforge.fetch('cattle_animals'));
        },
        async addAnimal(animal) {
            return await withErrorHandling(window.insforge.insert('cattle_animals', animal));
        },
        async getMilk() {
            return await withErrorHandling(window.insforge.fetch('cattle_milk'));
        },
        async recordMilk(milk) {
            return await withErrorHandling(window.insforge.insert('cattle_milk', milk));
        },
        async getHealth() {
            return await withErrorHandling(window.insforge.fetch('cattle_health'));
        },
        async addHealthRecord(record) {
            return await withErrorHandling(window.insforge.insert('cattle_health', record));
        },
        async getBreeding() {
            return await withErrorHandling(window.insforge.fetch('cattle_breeding'));
        },
        async getFeed() {
            return await withErrorHandling(window.insforge.fetch('cattle_feed'));
        },
        // Advanced Analytics
        async getMilkAnalytics(month, year) {
            const { data } = await withErrorHandling(window.insforge.fetch('cattle_milk'));
            const filtered = data?.filter(m => {
                const d = new Date(m.date);
                return d.getMonth() + 1 === month && d.getFullYear() === year;
            }) || [];

            const totalLiters = filtered.reduce((sum, m) => sum + (parseFloat(m.quantity_liters) || 0), 0);
            const avgFat = filtered.length ? filtered.reduce((s, m) => s + (parseFloat(m.fat_percent) || 0), 0) / filtered.length : 0;
            const avgSNF = filtered.length ? filtered.reduce((s, m) => s + (parseFloat(m.snf_percent) || 0), 0) / filtered.length : 0;
            const totalRevenue = filtered.reduce((sum, m) => sum + (parseFloat(m.quantity_liters) * parseFloat(m.rate) || 0), 0);

            return { data: { totalLiters: totalLiter.toFixed(2), avgFat: avgFat.toFixed(2), avgSNF: avgSNF.toFixed(2), revenue: totalRevenue.toFixed(2) } };
        },
        async getAnimalHealthSummary() {
            const { data: animals } = await withErrorHandling(window.insforge.fetch('cattle_animals'));
            const { data: health } = await withErrorHandling(window.insforge.fetch('cattle_health'));

            const total = animals?.length || 0;
            const last30Days = new Date();
            last30Days.setDate(last30Days.getDate() - 30);
            const recentHealth = health?.filter(h => new Date(h.date) >= last30Days) || [];
            const sick = new Set(recentHealth.map(h => h.animal_id)).size;

            return { data: { total, healthy: total - sick, sick, healthRate: total > 0 ? ((total - sick) / total * 100).toFixed(1) : 0 } };
        },
        async getBreedingStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('cattle_breeding'));
            const pregnant = data?.filter(b => b.status === 'pregnant').length || 0;
            const calved = data?.filter(b => b.status === 'calved').length || 0;
            const pending = data?.filter(b => b.status === 'pending').length || 0;

            return { data: { pregnant, calved, pending, successRate: (data?.length ? (calved / data.length * 100).toFixed(1) : 0) } };
        }
    };

    // ============================================
    // 14. VERMICULTURE MODULE
    // ============================================
    window.dbVermi = {
        async getBeds() {
            return await withErrorHandling(window.insforge.fetch('vermi_beds'));
        },
        async addBed(bed) {
            return await withErrorHandling(window.insforge.insert('vermi_beds', bed));
        },
        async getProduction() {
            return await withErrorHandling(window.insforge.fetch('vermi_production'));
        },
        async recordProduction(production) {
            return await withErrorHandling(window.insforge.insert('vermi_production', production));
        },
        async getSales() {
            return await withErrorHandling(window.insforge.fetch('vermi_sales'));
        }
    };

    // ============================================
    // 15. TREE/NURSERY MODULE
    // ============================================
    window.dbTree = {
        async getSpecies() {
            return await withErrorHandling(window.insforge.fetch('tree_species'));
        },
        async addSpecies(species) {
            return await withErrorHandling(window.insforge.insert('tree_species', species));
        },
        async getSaplings() {
            return await withErrorHandling(window.insforge.fetch('tree_saplings'));
        },
        async addSapling(sapling) {
            return await withErrorHandling(window.insforge.insert('tree_saplings', sapling));
        },
        async getSales() {
            return await withErrorHandling(window.insforge.fetch('tree_sales'));
        }
    };

    // ============================================
    // 16. AQUACULTURE MODULE
    // ============================================
    window.dbAqua = {
        async getPonds() {
            return await withErrorHandling(window.insforge.fetch('aqua_ponds'));
        },
        async addPond(pond) {
            return await withErrorHandling(window.insforge.insert('aqua_ponds', pond));
        },
        async getBatches() {
            return await withErrorHandling(window.insforge.fetch('aqua_batches'));
        },
        async addBatch(batch) {
            return await withErrorHandling(window.insforge.insert('aqua_batches', batch));
        },
        async getFeed() {
            return await withErrorHandling(window.insforge.fetch('aqua_feed'));
        },
        async getHealth() {
            return await withErrorHandling(window.insforge.fetch('aqua_health'));
        },
        async getHarvest() {
            return await withErrorHandling(window.insforge.fetch('aqua_harvest'));
        },
        // Advanced Analytics
        async getBatchPerformance(batchId) {
            const { data: batch } = await withErrorHandling(window.insforge.fetch('aqua_batches'));
            const { data: feed } = await withErrorHandling(window.insforge.fetch('aqua_feed'));
            const { data: harvest } = await withErrorHandling(window.insforge.fetch('aqua_harvest'));

            const b = batch?.find(b => b.id === batchId);
            if (!b) return { data: null };

            const totalFeed = feed?.filter(f => f.batch_id === batchId)
                .reduce((sum, f) => sum + (parseFloat(f.quantity_kg) || 0), 0) || 0;
            const totalHarvest = harvest?.filter(h => h.batch_id === batchId)
                .reduce((sum, h) => sum + (parseFloat(h.quantity_kg) || 0), 0) || 0;
            const seedCount = b.seed_count || 0;

            const survivalRate = seedCount > 0 ? ((totalHarvest / seedCount) * 100).toFixed(1) : 0;
            const fcr = totalHarvest > 0 ? (totalFeed / totalHarvest).toFixed(2) : 0;
            const avgWeight = totalHarvest > 0 ? (totalHarvest / totalHarvest).toFixed(2) : 0; // Simplified

            return { data: { seedCount, totalFeed, totalHarvest, survivalRate, fcr } };
        },
        async getWaterQualityStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('aqua_health'));
            const issues = data?.filter(h => h.disease && h.disease.includes('water')) || [];
            const diseaseCount = {};
            data?.forEach(h => {
                if (h.disease) diseaseCount[h.disease] = (diseaseCount[h.disease] || 0) + 1;
            });

            return { data: { totalRecords: data?.length || 0, waterIssues: issues.length, diseaseBreakdown: diseaseCount } };
        }
    };

    // ============================================
    // 17. VETERINARY HOSPITAL MODULE
    // ============================================
    window.dbVet = {
        async getAppointments(date) {
            const { data } = await withErrorHandling(window.insforge.fetch('vet_appointments'));
            return { data: date ? data?.filter(a => a.date === date) : data };
        },
        async createAppointment(appointment) {
            return await withErrorHandling(window.insforge.insert('vet_appointments', appointment));
        },
        async getPatients() {
            return await withErrorHandling(window.insforge.fetch('vet_patients'));
        },
        async addPatient(patient) {
            return await withErrorHandling(window.insforge.insert('vet_patients', patient));
        },
        async getRecords(patientId) {
            const { data } = await withErrorHandling(window.insforge.fetch('vet_records'));
            return { data: patientId ? data?.filter(r => r.patient_id === patientId) : data };
        },
        async addRecord(record) {
            return await withErrorHandling(window.insforge.insert('vet_records', record));
        }
    };

    // ============================================
    // 18. VEDIC HUB MODULE
    // ============================================
    window.dbVedic = {
        async getCourses() {
            return await withErrorHandling(window.insforge.fetch('vedic_courses'));
        },
        async getEnrollments() {
            return await withErrorHandling(window.insforge.fetch('vedic_enrollments'));
        },
        async getEvents() {
            return await withErrorHandling(window.insforge.fetch('vedic_events'));
        }
    };

    // ============================================
    // 19. LOGISTICS MODULE
    // ============================================
    window.dbLogistics = {
        async getVehicles() {
            return await withErrorHandling(window.insforge.fetch('logistics_vehicles'));
        },
        async getTrips() {
            return await withErrorHandling(window.insforge.fetch('logistics_trips'));
        },
        async createTrip(trip) {
            return await withErrorHandling(window.insforge.insert('logistics_trips', trip));
        },
        async getDrivers() {
            return await withErrorHandling(window.insforge.fetch('logistics_drivers'));
        }
    };

    // ============================================
    // 20. WATER MANAGEMENT MODULE
    // ============================================
    window.dbWater = {
        async getSources() {
            return await withErrorHandling(window.insforge.fetch('water_sources'));
        },
        async getReadings() {
            return await withErrorHandling(window.insforge.fetch('water_readings'));
        },
        async addReading(reading) {
            return await withErrorHandling(window.insforge.insert('water_readings', reading));
        },
        async getUsage() {
            return await withErrorHandling(window.insforge.fetch('water_usage'));
        }
    };

    // ============================================
    // 21. TRUST MANAGEMENT MODULE
    // ============================================
    window.dbTrust = {
        async getMembers() {
            return await withErrorHandling(window.insforge.fetch('trust_members'));
        },
        async addMember(member) {
            return await withErrorHandling(window.insforge.insert('trust_members', member));
        },
        async getMeetings() {
            return await withErrorHandling(window.insforge.fetch('trust_meetings'));
        },
        async getDonations() {
            return await withErrorHandling(window.insforge.fetch('trust_donations'));
        }
    };

    // ============================================
    // 22. COMMAND CENTER MODULE
    // ============================================
    window.dbCommand = {
        async getAlerts() {
            return await withErrorHandling(window.insforge.fetch('command_alerts'));
        },
        async getMetrics() {
            return await withErrorHandling(window.insforge.fetch('command_metrics'));
        },
        async getActivities() {
            return await withErrorHandling(window.insforge.fetch('command_activities'));
        }
    };

    // ============================================
    // ERP MODULES (Already implemented above, adding missing functions)
    // ============================================

    // HRM - Add more functions
    window.dbHRM = {
        async getEmployees() {
            return await withErrorHandling(window.insforge.fetch('hrm_employees'));
        },
        async addEmployee(emp) {
            return await withErrorHandling(window.insforge.insert('hrm_employees', {
                ...emp,
                created_at: new Date().toISOString()
            }));
        },
        async getAttendance(date) {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_attendance'));
            return { data: date ? data?.filter(a => a.date === date) : data };
        },
        async markAttendance(attendance) {
            return await withErrorHandling(window.insforge.insert('hrm_attendance', attendance));
        },
        async getLeaves(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_leaves'));
            return { data: status ? data?.filter(l => l.status === status) : data };
        },
        async applyLeave(leave) {
            return await withErrorHandling(window.insforge.insert('hrm_leaves', leave));
        },
        async getPayroll() {
            return await withErrorHandling(window.insforge.fetch('hrm_payroll'));
        },
        // Advanced HRM Functions
        async getEmployeeCount() {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_employees'));
            const active = data?.filter(e => e.status === 'active').length || 0;
            const total = data?.length || 0;
            return { data: { active, total, inactive: total - active } };
        },
        async getAttendanceStats(employeeId, month, year) {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_attendance'));
            const filtered = data?.filter(a => {
                const d = new Date(a.date);
                return a.employee_id === employeeId && d.getMonth() + 1 === month && d.getFullYear() === year;
            }) || [];

            const present = filtered.filter(a => a.status === 'present').length;
            const absent = filtered.filter(a => a.status === 'absent').length;
            const total = filtered.length;

            return { data: { present, absent, total, attendanceRate: total > 0 ? (present / total * 100).toFixed(1) : 0 } };
        },
        async getLeaveBalance(employeeId) {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_leaves'));
            const leaves = data?.filter(l => l.employee_id === employeeId && l.status === 'approved') || [];

            const totalDays = leaves.reduce((sum, l) => sum + (parseFloat(l.days) || 0), 0);
            const casual = leaves.filter(l => l.leave_type === 'casual').reduce((s, l) => s + (parseFloat(l.days) || 0), 0);
            const sick = leaves.filter(l => l.leave_type === 'sick').reduce((s, l) => s + (parseFloat(l.days) || 0), 0);

            return {
                data: {
                    taken: totalDays,
                    casual,
                    sick,
                    casualRemaining: 12 - casual,
                    sickRemaining: 10 - sick
                }
            };
        },
        async calculatePayroll(month, year) {
            const { data: employees } = await withErrorHandling(window.insforge.fetch('hrm_employees'));
            const { data: leaves } = await withErrorHandling(window.insforge.fetch('hrm_leaves'));
            const { data: attendance } = await withErrorHandling(window.insforge.fetch('hrm_attendance'));

            const activeEmployees = employees?.filter(e => e.status === 'active') || [];

            const payroll = activeEmployees.map(emp => {
                const empLeaves = leaves?.filter(l =>
                    l.employee_id === emp.employee_id &&
                    l.status === 'approved' &&
                    new Date(l.start_date).getMonth() + 1 === month &&
                    new Date(l.start_date).getFullYear() === year
                ) || [];

                const leaveDays = empLeaves.reduce((sum, l) => sum + (parseFloat(l.days) || 0), 0);
                const basicSalary = parseFloat(emp.salary) || 0;
                const deduction = leaveDays * (basicSalary / 30);

                return {
                    employee_id: emp.employee_id,
                    name: emp.first_name + ' ' + emp.last_name,
                    department: emp.department,
                    basic_salary: basicSalary,
                    leave_deduction: deduction.toFixed(2),
                    net_pay: (basicSalary - deduction).toFixed(2)
                };
            });

            return { data: payroll };
        },
        async getDepartmentStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('hrm_employees'));
            const byDept = {};
            data?.forEach(e => {
                byDept[e.department] = (byDept[e.department] || 0) + 1;
            });
            return { data: byDept };
        }
    };

    // Inventory
    window.dbInventory = {
        async getProducts() {
            return await withErrorHandling(window.insforge.fetch('inv_products'));
        },
        async addProduct(product) {
            return await withErrorHandling(window.insforge.insert('inv_products', product));
        },
        async getPurchaseOrders() {
            return await withErrorHandling(window.insforge.fetch('inv_purchase_orders'));
        },
        async createPO(po) {
            return await withErrorHandling(window.insforge.insert('inv_purchase_orders', po));
        },
        async getLowStock() {
            const { data } = await withErrorHandling(window.insforge.fetch('inv_products'));
            return { data: data?.filter(p => p.current_stock <= p.reorder_level) || [] };
        },
        // Advanced Inventory Functions
        async getInventoryValue() {
            const { data } = await withErrorHandling(window.insforge.fetch('inv_products'));
            const totalValue = data?.reduce((sum, p) => sum + ((p.current_stock || 0) * (parseFloat(p.cost_price) || 0)), 0) || 0;
            const totalItems = data?.reduce((sum, p) => sum + (p.current_stock || 0), 0) || 0;
            return { data: { totalValue: totalValue.toFixed(2), totalItems, productCount: data?.length || 0 } };
        },
        async getStockAlerts() {
            const { data } = await withErrorHandling(window.insforge.fetch('inv_products'));
            const lowStock = data?.filter(p => p.current_stock <= p.reorder_level) || [];
            const outOfStock = data?.filter(p => p.current_stock === 0) || [];
            const overStock = data?.filter(p => p.current_stock > p.min_stock * 3) || [];

            return { data: { lowStock: lowStock.length, outOfStock: outOfStock.length, overStock: overStock.length } };
        },
        async getCategoryBreakdown() {
            const { data } = await withErrorHandling(window.insforge.fetch('inv_products'));
            const byCategory = {};
            data?.forEach(p => {
                byCategory[p.category] = (byCategory[p.category] || 0) + 1;
            });
            return { data: byCategory };
        },
        async getPurchaseAnalytics() {
            const { data } = await withErrorHandling(window.insforge.fetch('inv_purchase_orders'));
            const pending = data?.filter(po => po.status === 'pending').length || 0;
            const completed = data?.filter(po => po.status === 'completed').length || 0;
            const totalValue = data?.reduce((sum, po) => sum + (parseFloat(po.total_amount) || 0), 0) || 0;

            return { data: { pending, completed, totalValue: totalValue.toFixed(2), orderCount: data?.length || 0 } };
        }
    };

    // Finance
    window.dbFinance = {
        async getInvoices(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('fin_invoices'));
            return { data: status ? data?.filter(i => i.status === status) : data };
        },
        async createInvoice(invoice) {
            return await withErrorHandling(window.insforge.insert('fin_invoices', invoice));
        },
        async getExpenses() {
            return await withErrorHandling(window.insforge.fetch('fin_expenses'));
        },
        async addExpense(expense) {
            return await withErrorHandling(window.insforge.insert('fin_expenses', expense));
        },
        // Advanced Finance Functions
        async getFinancialSummary(year, month) {
            const { data: invoices } = await withErrorHandling(window.insforge.fetch('fin_invoices'));
            const { data: expenses } = await withErrorHandling(window.insforge.fetch('fin_expenses'));

            const invTotal = invoices?.reduce((sum, inv) => sum + (parseFloat(inv.total) || 0), 0) || 0;
            const expTotal = expenses?.reduce((sum, exp) => sum + (parseFloat(exp.amount) || 0), 0) || 0;

            return {
                data: {
                    totalRevenue: invTotal,
                    totalExpenses: expTotal,
                    netProfit: invTotal - expTotal,
                    profitMargin: invTotal > 0 ? ((invTotal - expTotal) / invTotal * 100).toFixed(2) : 0
                }
            };
        },
        async getExpensesByCategory(startDate, endDate) {
            const { data } = await withErrorHandling(window.insforge.fetch('fin_expenses'));
            const filtered = data?.filter(e => {
                const d = new Date(e.date);
                return d >= new Date(startDate) && d <= new Date(endDate);
            }) || [];

            const byCategory = {};
            filtered.forEach(e => {
                byCategory[e.category] = (byCategory[e.category] || 0) + (parseFloat(e.amount) || 0);
            });
            return { data: byCategory };
        },
        async calculateTax(amount, taxRate = 18) {
            const cgst = (amount * taxRate / 100) / 2;
            const sgst = cgst;
            return {
                data: {
                    baseAmount: amount,
                    cgst: cgst.toFixed(2),
                    sgst: sgst.toFixed(2),
                    totalTax: (cgst + sgst).toFixed(2),
                    totalWithTax: (amount + cgst + sgst).toFixed(2)
                }
            };
        },
        async getCashFlow(startDate, endDate) {
            const { data: invoices } = await withErrorHandling(window.insforge.fetch('fin_invoices'));
            const { data: expenses } = await withErrorHandling(window.insforge.fetch('fin_expenses'));

            const cashIn = invoices?.filter(i => i.status === 'paid' && i.invoice_date >= startDate && i.invoice_date <= endDate)
                .reduce((sum, i) => sum + (parseFloat(i.total) || 0), 0) || 0;
            const cashOut = expenses?.filter(e => e.date >= startDate && e.date <= endDate)
                .reduce((sum, e) => sum + (parseFloat(e.amount) || 0), 0) || 0;

            return { data: { cashIn, cashOut, netFlow: cashIn - cashOut } };
        }
    };

    // DMS
    window.dbDMS = {
        async getDocuments() {
            return await withErrorHandling(window.insforge.fetch('dms_documents'));
        },
        async uploadDocument(doc) {
            return await withErrorHandling(window.insforge.insert('dms_documents', doc));
        },
        async searchDocuments(query) {
            const { data } = await withErrorHandling(window.insforge.fetch('dms_documents'));
            return {
                data: data?.filter(d =>
                    d.name?.toLowerCase().includes(query.toLowerCase()) ||
                    d.content?.toLowerCase().includes(query.toLowerCase())
                )
            };
        }
    };

    // Workflow
    window.dbWorkflow = {
        async getApprovals(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('workflow_approvals'));
            return { data: status ? data?.filter(a => a.status === status) : data };
        },
        async createApproval(approval) {
            return await withErrorHandling(window.insforge.insert('workflow_approvals', approval));
        },
        async updateStatus(id, status) {
            // Update logic
        },
        // Advanced Workflow Functions
        async getApprovalStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('workflow_approvals'));
            const pending = data?.filter(a => a.status === 'pending').length || 0;
            const approved = data?.filter(a => a.status === 'approved').length || 0;
            const rejected = data?.filter(a => a.status === 'rejected').length || 0;
            const totalValue = data?.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0) || 0;

            return { data: { pending, approved, rejected, totalValue: totalValue.toFixed(2), approvalRate: data?.length ? (approved / data.length * 100).toFixed(1) : 0 } };
        },
        async getPendingApprovals() {
            const { data } = await withErrorHandling(window.insforge.fetch('workflow_approvals'));
            return { data: data?.filter(a => a.status === 'pending').sort((a, b) => new Date(a.created_at) - new Date(b.created_at)) || [] };
        }
    };

    // Ticketing
    window.dbTicketing = {
        async getTickets(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('ticketing_tickets'));
            return { data: status ? data?.filter(t => t.status === status) : data };
        },
        async createTicket(ticket) {
            return await withErrorHandling(window.insforge.insert('ticketing_tickets', ticket));
        },
        async updateTicket(id, updates) {
            // Update logic
        },
        // Advanced Ticketing Functions
        async getTicketStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('ticketing_tickets'));
            const open = data?.filter(t => t.status === 'open').length || 0;
            const inProgress = data?.filter(t => t.status === 'in_progress').length || 0;
            const closed = data?.filter(t => t.status === 'closed').length || 0;
            const highPriority = data?.filter(t => t.priority === 'high').length || 0;

            return { data: { open, inProgress, closed, highPriority, resolutionRate: data?.length ? (closed / data.length * 100).toFixed(1) : 0 } };
        },
        async getSLACompliance() {
            const { data } = await withErrorHandling(window.insforge.fetch('ticketing_tickets'));
            const now = new Date();
            const overdue = data?.filter(t => {
                const created = new Date(t.created_at);
                const hours = (now - created) / (1000 * 60 * 60);
                return t.status !== 'closed' && hours > 24;
            }).length || 0;

            return { data: { overdue, total: data?.length || 0, complianceRate: data?.length ? ((data.length - overdue) / data.length * 100).toFixed(1) : 100 } };
        }
    };

    // BI
    window.dbBI = {
        async getAnalytics(module) {
            return await withErrorHandling(window.insforge.fetch('bi_analytics'));
        },
        async getReports() {
            return await withErrorHandling(window.insforge.fetch('bi_reports'));
        },
        // Advanced BI Functions
        async getCrossModuleSummary() {
            const { data: finance } = await withErrorHandling(window.insforge.fetch('fin_invoices'));
            const { data: hrm } = await withErrorHandling(window.insforge.fetch('hrm_employees'));
            const { data: inv } = await withErrorHandling(window.insforge.fetch('inv_products'));
            const { data: crm } = await withErrorHandling(window.insforge.fetch('crm_leads'));

            return {
                data: {
                    revenue: finance?.reduce((s, f) => s + (parseFloat(f.total) || 0), 0) || 0,
                    employees: hrm?.length || 0,
                    products: inv?.length || 0,
                    leads: crm?.length || 0
                }
            };
        }
    };

    // Booking (Tier 3)
    window.dbBooking = {
        async getBookings(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('bkg_bookings'));
            return { data };
        },
        async createBooking(booking) {
            return await withErrorHandling(window.insforge.insert('bkg_bookings', booking));
        },
        async getVetAppointments(date) {
            const { data } = await withErrorHandling(window.insforge.fetch('bkg_vet_appointments'));
            return { data: date ? data?.filter(a => a.date === date) : data };
        },
        // Advanced Booking Functions
        async getBookingStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('bkg_bookings'));
            const pending = data?.filter(b => b.status === 'pending').length || 0;
            const confirmed = data?.filter(b => b.status === 'confirmed').length || 0;
            const completed = data?.filter(b => b.status === 'completed').length || 0;
            const cancelled = data?.filter(b => b.status === 'cancelled').length || 0;
            const totalRevenue = data?.reduce((sum, b) => sum + (parseFloat(b.amount) || 0), 0) || 0;

            return { data: { pending, confirmed, completed, cancelled, totalRevenue: totalRevenue.toFixed(2) } };
        },
        async getUpcomingBookings(days = 7) {
            const { data } = await withErrorHandling(window.insforge.fetch('bkg_bookings'));
            const future = new Date();
            future.setDate(future.getDate() + days);

            return {
                data: data?.filter(b => {
                    const checkIn = new Date(b.check_in);
                    return checkIn <= future && (b.status === 'confirmed' || b.status === 'pending');
                }) || []
            };
        }
    };

    // LMS (Tier 3)
    window.dbLMS = {
        async getCourses() {
            return await withErrorHandling(window.insforge.fetch('lms_courses'));
        },
        async createCourse(course) {
            return await withErrorHandling(window.insforge.insert('lms_courses', course));
        },
        async getEnrollments(userId) {
            const { data } = await withErrorHandling(window.insforge.fetch('lms_enrollments'));
            return { data: userId ? data?.filter(e => e.user_id === userId) : data };
        },
        // Advanced LMS Functions
        async getCourseAnalytics() {
            const { data: courses } = await withErrorHandling(window.insforge.fetch('lms_courses'));
            const { data: enrollments } = await withErrorHandling(window.insforge.fetch('lms_enrollments'));

            const activeCourses = courses?.filter(c => c.status === 'active').length || 0;
            const totalEnrollments = enrollments?.length || 0;
            const completed = enrollments?.filter(e => e.progress_percentage === 100).length || 0;
            const inProgress = enrollments?.filter(e => e.progress_percentage > 0 && e.progress_percentage < 100).length || 0;

            return { data: { activeCourses, totalEnrollments, completed, inProgress, completionRate: totalEnrollments ? (completed / totalEnrollments * 100).toFixed(1) : 0 } };
        },
        async getUserProgress(userId) {
            const { data } = await withErrorHandling(window.insforge.fetch('lms_enrollments'));
            const userEnroll = data?.filter(e => e.user_id === userId) || [];
            const avgProgress = userEnroll.length ? userEnroll.reduce((s, e) => s + (e.progress_percentage || 0), 0) / userEnroll.length : 0;

            return { data: { courses: userEnroll.length, avgProgress: avgProgress.toFixed(1) } };
        }
    };

    // Field Service (Tier 3)
    window.dbFieldService = {
        async getJobs(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('fs_jobs'));
            return { data: status ? data?.filter(j => j.status === status) : data };
        },
        async createJob(job) {
            return await withErrorHandling(window.insforge.insert('fs_jobs', job));
        },
        // Advanced Field Service Functions
        async getJobStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('fs_jobs'));
            const scheduled = data?.filter(j => j.status === 'scheduled').length || 0;
            const inProgress = data?.filter(j => j.status === 'in_progress').length || 0;
            const completed = data?.filter(j => j.status === 'completed').length || 0;
            const cancelled = data?.filter(j => j.status === 'cancelled').length || 0;

            return { data: { scheduled, inProgress, completed, cancelled, total: data?.length || 0 } };
        },
        async getOverdueJobs() {
            const { data } = await withErrorHandling(window.insforge.fetch('fs_jobs'));
            const today = new Date().toISOString().split('T')[0];

            return { data: data?.filter(j => j.scheduled_date < today && j.status === 'scheduled') || [] };
        }
    };

    // Farmer Portal (Tier 3)
    window.dbFarmer = {
        async getFarmers() {
            return await withErrorHandling(window.insforge.fetch('fp_farmers'));
        },
        async registerFarmer(farmer) {
            return await withErrorHandling(window.insforge.insert('fp_farmers', farmer));
        },
        async getCrops(farmerId) {
            const { data } = await withErrorHandling(window.insforge.fetch('fp_crops'));
            return { data: farmerId ? data?.filter(c => c.farmer_id === farmerId) : data };
        },
        // Advanced Farmer Portal Functions
        async getFarmerStats() {
            const { data } = await withErrorHandling(window.insforge.fetch('fp_farmers'));
            const { data: crops } = await withErrorHandling(window.insforge.fetch('fp_crops'));

            const totalAcres = data?.reduce((sum, f) => sum + (parseFloat(f.total_acres) || 0), 0) || 0;
            const activeCrops = crops?.filter(c => c.status === 'active').length || 0;

            return { data: { totalFarmers: data?.length || 0, totalAcres: totalAcres.toFixed(2), activeCrops } };
        },
        async getCropSummary() {
            const { data } = await withErrorHandling(window.insforge.fetch('fp_crops'));
            const byCrop = {};
            data?.forEach(c => {
                byCrop[c.crop_name] = (byCrop[c.crop_name] || 0) + (parseFloat(c.acres) || 0);
            });
            return { data: byCrop };
        }
    };

    // Survey (Tier 3)
    window.dbSurvey = {
        async getSurveys(status) {
            const { data } = await withErrorHandling(window.insforge.fetch('sur_surveys'));
            return { data: status ? data?.filter(s => s.status === status) : data };
        },
        async createSurvey(survey) {
            return await withErrorHandling(window.insforge.insert('sur_surveys', survey));
        },
        async getResponses(surveyId) {
            const { data } = await withErrorHandling(window.insforge.fetch('sur_responses'));
            return { data: surveyId ? data?.filter(r => r.survey_id === surveyId) : data };
        },
        // Advanced Survey Functions
        async getSurveyAnalytics() {
            const { data: surveys } = await withErrorHandling(window.insforge.fetch('sur_surveys'));
            const { data: responses } = await withErrorHandling(window.insforge.fetch('sur_responses'));

            const active = surveys?.filter(s => s.status === 'active').length || 0;
            const draft = surveys?.filter(s => s.status === 'draft').length || 0;
            const totalResponses = responses?.length || 0;
            const avgRating = responses?.length ? responses.reduce((s, r) => s + (r.rating || 0), 0) / responses.length : 0;

            return { data: { active, draft, totalResponses, avgRating: avgRating.toFixed(1) } };
        },
        async getNPS() {
            const { data } = await withErrorHandling(window.insforge.fetch('sur_responses'));
            const promoters = data?.filter(r => r.rating >= 9).length || 0;
            const detractors = data?.filter(r => r.rating <= 6).length || 0;
            const total = data?.length || 0;
            const nps = total ? ((promoters - detractors) / total * 100).toFixed(0) : 0;

            return { data: { nps, promoters, detractors, total } };
        }
    };

    // Schemes (Tier 3)
    window.dbSchemes = {
        async getSchemes() {
            return await withErrorHandling(window.insforge.fetch('sch_schemes'));
        },
        async getApplications(farmerId) {
            const { data } = await withErrorHandling(window.insforge.fetch('sch_applications'));
            return { data: farmerId ? data?.filter(a => a.farmer_id === farmerId) : data };
        },
        async applyForScheme(application) {
            return await withErrorHandling(window.insforge.insert('sch_applications', application));
        },
        // Advanced Schemes Functions
        async getSchemeStats() {
            const { data: schemes } = await withErrorHandling(window.insforge.fetch('sch_schemes'));
            const { data: applications } = await withErrorHandling(window.insforge.fetch('sch_applications'));

            const activeSchemes = schemes?.filter(s => s.status === 'active').length || 0;
            const pending = applications?.filter(a => a.status === 'pending').length || 0;
            const approved = applications?.filter(a => a.status === 'approved').length || 0;
            const rejected = applications?.filter(a => a.status === 'rejected').length || 0;
            const totalAmount = applications?.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0) || 0;

            return { data: { activeSchemes, pending, approved, rejected, totalAmount: totalAmount.toFixed(2) } };
        },
        async getDisbursementStatus() {
            const { data } = await withErrorHandling(window.insforge.fetch('sch_applications'));
            const disbursed = data?.filter(a => a.disbursement_status === 'disbursed').length || 0;
            const pendingDisbursement = data?.filter(a => a.status === 'approved' && a.disbursement_status !== 'disbursed').length || 0;

            return { data: { disbursed, pendingDisbursement } };
        }
    };

    // ============================================
    // GLOBAL DB OBJECT - All modules
    // ============================================
    window.addEventListener('DOMContentLoaded', async function () {
        console.log('Complete Database Integration Layer Loaded');

        window.db = {
            // Energy & Infrastructure
            tourism: window.dbTourism,
            carbon: window.dbCarbon,
            paint: window.dbPaint,
            grid: window.dbGrid,
            solar: window.dbSolar,
            wind: window.dbWind,
            biogas: window.dbBiogas,
            hydrogen: window.dbHydrogen,
            hydro: window.dbHydro,
            kinetic: window.dbKinetic,

            // Agriculture & Livestock
            cattle: window.dbCattle,
            poultry: window.dbPoultry,
            aqua: window.dbAqua,
            vermi: window.dbVermi,
            tree: window.dbTree,

            // Services
            vet: window.dbVet,
            vedic: window.dbVedic,
            logistics: window.dbLogistics,

            // Operations
            water: window.dbWater,
            trust: window.dbTrust,
            command: window.dbCommand,

            // ERP
            crm: window.dbCRM,
            hrm: window.dbHRM,
            inventory: window.dbInventory,
            finance: window.dbFinance,
            dms: window.dbDMS,
            workflow: window.dbWorkflow,
            ticketing: window.dbTicketing,
            bi: window.dbBI,

            // Tier 3
            booking: window.dbBooking,
            lms: window.dbLMS,
            fieldService: window.dbFieldService,
            farmer: window.dbFarmer,
            survey: window.dbSurvey,
            schemes: window.dbSchemes
        };

        console.log('Available db modules:', Object.keys(window.db));
    });

    // Helper function to load data
    window.loadTableData = async function (tableId, dataLoader) {
        try {
            const { data, error } = await dataLoader();
            if (error) {
                console.error('Error:', error);
                return;
            }
            const table = document.getElementById(tableId);
            if (table && table.querySelector('tbody')) {
                const tbody = table.querySelector('tbody');
                tbody.innerHTML = '';
                (data || []).forEach(item => {
                    const row = document.createElement('tr');
                    Object.values(item).forEach(val => {
                        const cell = document.createElement('td');
                        cell.textContent = val || '-';
                        row.appendChild(cell);
                    });
                    tbody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error loading table:', error);
        }
    };

    console.log('Complete Database Integration Layer Initialized');

} catch (e) {
    console.error('DB Integration Error:', e);
}
