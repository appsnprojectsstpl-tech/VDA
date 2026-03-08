// TPL:booking
booking: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>📅 Booking &amp; Reservations</h2>
                <button class="crm-btn" onclick="bookingTab('all-bookings', this)">+ New Booking</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="bookingTab('all-bookings', this)">All Bookings</button>
                <button class="crm-tab-btn" onclick="bookingTab('agri-tourism', this)">Agri-Tourism</button>
                <button class="crm-tab-btn" onclick="bookingTab('vet-appointments', this)">Vet Appointments</button>
                <button class="crm-tab-btn" onclick="bookingTab('events', this)">Events</button>
                <button class="crm-tab-btn" onclick="bookingTab('calendar', this)">Calendar</button>
            </div>
            <div id="booking-all-bookings" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">📅</span><span class="kpi-val">127</span><span class="kpi-lbl">Total Bookings</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">89</span><span class="kpi-lbl">Confirmed</span></div>
                    <div class="kpi-card"><span class="kpi-icon">⏳</span><span class="kpi-val">23</span><span class="kpi-lbl">Pending</span></div>
                    <div class="kpi-card"><span class="kpi-icon">💰</span><span class="kpi-val">₹4.2L</span><span class="kpi-lbl">Revenue</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>ID</th><th>Guest</th><th>Type</th><th>Check-in</th><th>Check-out</th><th>Status</th><th>Amount</th></tr></thead>
                    <tbody>
                        <tr><td>BK-001</td><td>Rajesh Kumar</td><td>Agri-Tourism</td><td>2026-03-01</td><td>2026-03-03</td><td><span class="pill confirmed">Confirmed</span></td><td>₹15,000</td></tr>
                        <tr><td>BK-002</td><td>Priya Sharma</td><td>Vet Appointment</td><td>2026-03-05</td><td>2026-03-05</td><td><span class="pill pending">Pending</span></td><td>₹500</td></tr>
                        <tr><td>BK-003</td><td>Mahesh Reddy</td><td>Agri-Tourism</td><td>2026-03-10</td><td>2026-03-12</td><td><span class="pill confirmed">Confirmed</span></td><td>₹22,500</td></tr>
                    </tbody>
                </table>
            </div>
            <div id="booking-agri-tourism" class="crm-tab-content"><h3>🌾 Agri-Tourism Bookings</h3><p>Agri-tourism bookings management.</p></div>
            <div id="booking-vet-appointments" class="crm-tab-content"><h3>🏥 Vet Appointments</h3><p>Veterinary appointment booking system.</p></div>
            <div id="booking-events" class="crm-tab-content"><h3>🎉 Event Reservations</h3><p>Event booking and management.</p></div>
            <div id="booking-calendar" class="crm-tab-content"><h3>📆 Booking Calendar</h3><p>Calendar view of all bookings.</p></div>
        </div>
    `

// TPL:lms
lms: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>🎓 Learning Management System</h2>
                <button class="crm-btn" onclick="lmsTab('courses', this)">+ Create Course</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="lmsTab('courses', this)">Courses</button>
                <button class="crm-tab-btn" onclick="lmsTab('my-learning', this)">My Learning</button>
                <button class="crm-tab-btn" onclick="lmsTab('certifications', this)">Certifications</button>
                <button class="crm-tab-btn" onclick="lmsTab('assessments', this)">Assessments</button>
                <button class="crm-tab-btn" onclick="lmsTab('analytics', this)">Analytics</button>
            </div>
            <div id="lms-courses" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">📚</span><span class="kpi-val">24</span><span class="kpi-lbl">Total Courses</span></div>
                    <div class="kpi-card"><span class="kpi-icon">👥</span><span class="kpi-val">156</span><span class="kpi-lbl">Enrolled</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">89</span><span class="kpi-lbl">Completed</span></div>
                    <div class="kpi-card"><span class="kpi-icon">⭐</span><span class="kpi-val">4.5</span><span class="kpi-lbl">Avg Rating</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Course</th><th>Category</th><th>Modules</th><th>Instructor</th><th>Rating</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>Organic Farming Basics</td><td>Agriculture</td><td>12</td><td>Dr. Ramasamy</td><td>4.5 ⭐</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>Cattle Management</td><td>Livestock</td><td>8</td><td>Dr. Srinivas</td><td>4.8 ⭐</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>Vet First Aid</td><td>Veterinary</td><td>10</td><td>Dr. Padma</td><td>4.6 ⭐</td><td><span class="pill confirmed">Active</span></td></tr>
                    </tbody>
                </table>
            </div>
            <div id="lms-my-learning" class="crm-tab-content"><h3>📖 My Enrolled Courses</h3></div>
            <div id="lms-certifications" class="crm-tab-content"><h3>🏆 My Certifications</h3></div>
            <div id="lms-assessments" class="crm-tab-content"><h3>📝 Assessments</h3></div>
            <div id="lms-analytics" class="crm-tab-content"><h3>📊 Learning Analytics</h3></div>
        </div>
    `

// TPL:fieldservice
fieldservice: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>🚜 Field Service Management</h2>
                <button class="crm-btn" onclick="fsTab('all-jobs', this)">+ New Job</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="fsTab('all-jobs', this)">All Jobs</button>
                <button class="crm-tab-btn" onclick="fsTab('scheduled', this)">Scheduled</button>
                <button class="crm-tab-btn" onclick="fsTab('in-progress', this)">In Progress</button>
                <button class="crm-tab-btn" onclick="fsTab('completed', this)">Completed</button>
                <button class="crm-tab-btn" onclick="fsTab('field-map', this)">Field Map</button>
            </div>
            <div id="fs-all-jobs" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">📋</span><span class="kpi-val">89</span><span class="kpi-lbl">Total Jobs</span></div>
                    <div class="kpi-card"><span class="kpi-icon">⏳</span><span class="kpi-val">23</span><span class="kpi-lbl">Pending</span></div>
                    <div class="kpi-card"><span class="kpi-icon">🔄</span><span class="kpi-val">12</span><span class="kpi-lbl">In Progress</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">54</span><span class="kpi-lbl">Completed</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Job ID</th><th>Service</th><th>Location</th><th>Farmer</th><th>Team</th><th>Date</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>FS-001</td><td>Soil Testing</td><td>Kuppam</td><td>Ramu</td><td>Team A</td><td>Mar 01</td><td><span class="pill pending">Scheduled</span></td></tr>
                        <tr><td>FS-002</td><td>Crop Inspection</td><td>Palamaner</td><td>Lakshman</td><td>Team B</td><td>Mar 01</td><td><span class="pill confirmed">In Progress</span></td></tr>
                        <tr><td>FS-003</td><td>Equipment Repair</td><td>Bangarupalem</td><td>Venkatesh</td><td>Tech Team</td><td>Feb 28</td><td><span class="pill confirmed">Completed</span></td></tr>
                    </tbody>
                </table>
            </div>
            <div id="fs-scheduled" class="crm-tab-content"><h3>📅 Scheduled Jobs</h3></div>
            <div id="fs-in-progress" class="crm-tab-content"><h3>🔄 Active Jobs</h3></div>
            <div id="fs-completed" class="crm-tab-content"><h3>✅ Completed Jobs</h3></div>
            <div id="fs-field-map" class="crm-tab-content"><h3>🗺️ Field Map</h3></div>
        </div>
    `

// TPL:farmerportal
farmerportal: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>👨‍🌾 Farmer Portal</h2>
                <button class="crm-btn" onclick="fpTab('dashboard', this)">My Farm</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="fpTab('dashboard', this)">Dashboard</button>
                <button class="crm-tab-btn" onclick="fpTab('crops', this)">My Crops</button>
                <button class="crm-tab-btn" onclick="fpTab('livestock', this)">Livestock</button>
                <button class="crm-tab-btn" onclick="fpTab('schemes', this)">Schemes</button>
                <button class="crm-tab-btn" onclick="fpTab('market', this)">Market Prices</button>
            </div>
            <div id="fp-dashboard" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">🌾</span><span class="kpi-val">12</span><span class="kpi-lbl">Acres Cultivated</span></div>
                    <div class="kpi-card"><span class="kpi-icon">🐄</span><span class="kpi-val">8</span><span class="kpi-lbl">Livestock</span></div>
                    <div class="kpi-card"><span class="kpi-icon">💰</span><span class="kpi-val">₹2.4L</span><span class="kpi-lbl">This Season</span></div>
                    <div class="kpi-card"><span class="kpi-icon">📋</span><span class="kpi-val">3</span><span class="kpi-lbl">Pending Tasks</span></div>
                </div>
                <div class="farmer-alerts" style="margin-top:1rem;padding:1rem;background:#0a1a10;border-radius:8px;">
                    <h4>🔔 Alerts</h4>
                    <div class="alert-item" style="padding:.5rem;margin:.3rem 0;background:#1a2f1a;border-radius:4px;">🌧️ Weather Alert: Heavy rain expected Mar 05</div>
                    <div class="alert-item" style="padding:.5rem;margin:.3rem 0;background:#1a2f1a;border-radius:4px;">✅ Soil test results available for Plot #3</div>
                    <div class="alert-item" style="padding:.5rem;margin:.3rem 0;background:#1a2f1a;border-radius:4px;">📅 Vaccination camp on Mar 10</div>
                </div>
            </div>
            <div id="fp-crops" class="crm-tab-content"><h3>🌾 My Crops</h3></div>
            <div id="fp-livestock" class="crm-tab-content"><h3>🐄 Livestock</h3></div>
            <div id="fp-schemes" class="crm-tab-content"><h3>🏛️ Government Schemes</h3></div>
            <div id="fp-market" class="crm-tab-content"><h3>💹 Market Prices</h3></div>
        </div>
    `

// TPL:survey
survey: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>📋 Survey &amp; Feedback</h2>
                <button class="crm-btn" onclick="surveyTab('surveys', this)">+ New Survey</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="surveyTab('surveys', this)">All Surveys</button>
                <button class="crm-tab-btn" onclick="surveyTab('farmer', this)">Farmer Surveys</button>
                <button class="crm-tab-btn" onclick="surveyTab('satisfaction', this)">Satisfaction</button>
                <button class="crm-tab-btn" onclick="surveyTab('analytics', this)">Analytics</button>
            </div>
            <div id="survey-surveys" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">📋</span><span class="kpi-val">24</span><span class="kpi-lbl">Total Surveys</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">1,456</span><span class="kpi-lbl">Responses</span></div>
                    <div class="kpi-card"><span class="kpi-icon">⭐</span><span class="kpi-val">4.3</span><span class="kpi-lbl">Avg Rating</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Survey</th><th>Type</th><th>Responses</th><th>Status</th><th>Action</th></tr></thead>
                    <tbody>
                        <tr><td>Farmer Satisfaction Q1</td><td>Satisfaction</td><td>234</td><td><span class="pill confirmed">Active</span></td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>Crop Advisory Feedback</td><td>Feedback</td><td>189</td><td><span class="pill confirmed">Active</span></td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>Vet Services Rating</td><td>Rating</td><td>302</td><td><span class="pill confirmed">Active</span></td><td><button class="action-btn">View</button></td></tr>
                    </tbody>
                </table>
            </div>
            <div id="survey-farmer" class="crm-tab-content"><h3>🌾 Farmer Surveys</h3></div>
            <div id="survey-satisfaction" class="crm-tab-content"><h3>⭐ Satisfaction Surveys</h3></div>
            <div id="survey-analytics" class="crm-tab-content"><h3>📊 Survey Analytics</h3></div>
        </div>
    `

// TPL:schemes
schemes: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>🏛️ Government Schemes</h2>
                <button class="crm-btn" onclick="schemeTab('schemes', this)">+ New Application</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="schemeTab('schemes', this)">All Schemes</button>
                <button class="crm-tab-btn" onclick="schemeTab('applications', this)">Applications</button>
                <button class="crm-tab-btn" onclick="schemeTab('disbursements', this)">Disbursements</button>
                <button class="crm-tab-btn" onclick="schemeTab('analytics', this)">Analytics</button>
            </div>
            <div id="scheme-schemes" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">🏛️</span><span class="kpi-val">18</span><span class="kpi-lbl">Active Schemes</span></div>
                    <div class="kpi-card"><span class="kpi-icon">📋</span><span class="kpi-val">456</span><span class="kpi-lbl">Applications</span></div>
                    <div class="kpi-card"><span class="kpi-icon">💰</span><span class="kpi-val">₹12.4L</span><span class="kpi-lbl">Disbursed</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">89%</span><span class="kpi-lbl">Approval Rate</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Scheme</th><th>Department</th><th>Benefit</th><th>Applicants</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>PM-KISAN</td><td>Agriculture</td><td>₹6000/year</td><td>234</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>Fasal Bima Yojana</td><td>Agriculture</td><td>Crop Insurance</td><td>189</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>NABARD Farm Loan</td><td>Finance</td><td>Up to ₹5L</td><td>67</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>Solar Pump Subsidy</td><td>Energy</td><td>90% Subsidy</td><td>45</td><td><span class="pill pending">Limited</span></td></tr>
                        <tr><td>Kisan Credit Card</td><td>Finance</td><td>Credit Facility</td><td>312</td><td><span class="pill confirmed">Active</span></td></tr>
                    </tbody>
                </table>
            </div>
            <div id="scheme-applications" class="crm-tab-content"><h3>📋 Scheme Applications</h3></div>
            <div id="scheme-disbursements" class="crm-tab-content"><h3>💰 Disbursements</h3></div>
            <div id="scheme-analytics" class="crm-tab-content"><h3>📊 Scheme Analytics</h3></div>
        </div>
    `
