#!/usr/bin/env python3
"""
Tier 3 Modules Injection Script
Adds Booking/Reservation, LMS, Field Service, Farmer Portal, Survey/Feedback, Government Schemes
"""

import re
import sys

def inject_tier3_modules():
    with open('dashboard/app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define new page templates to insert before the closing of pages object
    tier3_pages = '''

    // ============================================
    // TIER 3 - BOOKING & RESERVATION MODULE
    // ============================================
    booking: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>📅 Booking & Reservations</h2>
                <button class="crm-btn" onclick="bookingTab('all-bookings', this)">+ New Booking</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="bookingTab('all-bookings', this)">All Bookings</button>
                <button class="crm-tab-btn" onclick="bookingTab('agri-tourism', this)">Agri-Tourism</button>
                <button class="crm-tab-btn" onclick="bookingTab('vet-appointments', this)">Vet Appointments</button>
                <button class="crm-tab-btn" onclick="bookingTab('events', this)">Events</button>
                <button class="crm-tab-btn" onclick="bookingTab('calendar', this)">Calendar</button>
            </div>
            
            <!-- All Bookings Tab -->
            <div id="booking-all-bookings" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">📅</span>
                        <span class="kpi-val">127</span>
                        <span class="kpi-lbl">Total Bookings</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">✅</span>
                        <span class="kpi-val">89</span>
                        <span class="kpi-lbl">Confirmed</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">⏳</span>
                        <span class="kpi-val">23</span>
                        <span class="kpi-lbl">Pending</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">💰</span>
                        <span class="kpi-val">₹4.2L</span>
                        <span class="kpi-lbl">Revenue</span>
                    </div>
                </div>
                <table class="data-table">
                    <thead><tr><th>ID</th><th>Guest</th><th>Type</th><th>Check-in</th><th>Check-out</th><th>Status</th><th>Amount</th><th>Actions</th></tr></thead>
                    <tbody>
                        <tr><td>BK-001</td><td>Rajesh Kumar</td><td>Agri-Tourism</td><td>2026-03-01</td><td>2026-03-03</td><td><span class="pill confirmed">Confirmed</span></td><td>₹15,000</td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>BK-002</td><td>Priya Sharma</td><td>Vet Appointment</td><td>2026-03-05</td><td>2026-03-05</td><td><span class="pill pending">Pending</span></td><td>₹500</td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>BK-003</td><td>Mahesh Reddy</td><td>Agri-Tourism</td><td>2026-03-10</td><td>2026-03-12</td><td><span class="pill confirmed">Confirmed</span></td><td>₹22,500</td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>BK-004</td><td>Anita Desai</td><td>Event</td><td>2026-03-15</td><td>2026-03-15</td><td><span class="pill pending">Pending</span></td><td>₹50,000</td><td><button class="action-btn">View</button></td></tr>
                        <tr><td>BK-005</td><td>Vikram Singh</td><td>Agri-Tourism</td><td>2026-03-20</td><td>2026-03-22</td><td><span class="pill confirmed">Confirmed</span></td><td>₹18,000</td><td><button class="action-btn">View</button></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Agri-Tourism Tab -->
            <div id="booking-agri-tourism" class="crm-tab-content">
                <h3>🌾 Agri-Tourism Bookings</h3>
                <div class="filter-bar">
                    <input type="text" placeholder="Search guest..." class="search-input">
                    <select><option>All Status</option><option>Confirmed</option><option>Pending</option><option>Cancelled</option></select>
                    <button class="crm-btn">Export</button>
                </div>
                <table class="data-table">
                    <thead><tr><th>Booking ID</th><th>Guest Name</th><th>Package</th><th>Arrival</th><th>Departure</th><th>Guests</th><th>Amount</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>AT-2026-001</td><td>Rajesh Kumar</td><td>Farm Stay + Organic</td><td>Mar 01</td><td>Mar 03</td><td>4</td><td>₹15,000</td><td><span class="pill confirmed">Confirmed</span></td></tr>
                        <tr><td>AT-2026-002</td><td>Priya Sharma</td><td>Day Visit</td><td>Mar 08</td><td>Mar 08</td><td>2</td><td>₹3,000</td><td><span class="pill confirmed">Confirmed</span></td></tr>
                        <tr><td>AT-2026-003</td><td>Mahesh Reddy</td><td>Farm Stay Complete</td><td>Mar 10</td><td>Mar 12</td><td>6</td><td>₹22,500</td><td><span class="pill pending">Pending</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Vet Appointments Tab -->
            <div id="booking-vet-appointments" class="crm-tab-content">
                <h3>🏥 Veterinary Hospital Appointments</h3>
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">📅</span><span class="kpi-val">45</span><span class="kpi-lbl">Today</span></div>
                    <div class="kpi-card"><span class="kpi-icon">⏳</span><span class="kpi-val">12</span><span class="kpi-lbl">Pending</span></div>
                    <div class="kpi-card"><span class="kpi-icon">✅</span><span class="kpi-val">33</span><span class="kpi-lbl">Completed</span></div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Token</th><th>Owner</th><th>Animal</th><th>Type</th><th>Time</th><th>Doctor</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>VET-001</td><td>Ramu Naidu</td><td>Cow (Holstein)</td><td>Checkup</td><td>09:00 AM</td><td>Dr. Srinivas</td><td><span class="pill confirmed">Completed</span></td></tr>
                        <tr><td>VET-002</td><td>Lakshman</td><td>Buffalo</td><td>Vaccination</td><td>09:30 AM</td><td>Dr. Padma</td><td><span class="pill pending">Waiting</span></td></tr>
                        <tr><td>VET-003</td><td>Venkatesh</td><td>Goat</td><td>Surgery</td><td>10:00 AM</td><td>Dr. Srinivas</td><td><span class="pill pending">In Progress</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Events Tab -->
            <div id="booking-events" class="crm-tab-content">
                <h3>🎉 Event Reservations</h3>
                <button class="crm-btn">+ Create Event</button>
                <table class="data-table">
                    <thead><tr><th>Event</th><th>Date</th><th>Capacity</th><th>Booked</th><th>Revenue</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>Organic Farming Workshop</td><td>Mar 15, 2026</td><td>50</td><td>38</td><td>₹38,000</td><td><span class="pill confirmed">Open</span></td></tr>
                        <tr><td>Village Festival</td><td>Mar 22, 2026</td><td>200</td><td>156</td><td>₹1,56,000</td><td><span class="pill confirmed">Open</span></td></tr>
                        <tr><td>Cattle Exhibition</td><td>Apr 05, 2026</td><td>500</td><td>234</td><td>₹2,34,000</td><td><span class="pill pending">Promotion</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Calendar Tab -->
            <div id="booking-calendar" class="crm-tab-content">
                <h3>📆 Booking Calendar</h3>
                <div class="calendar-view">
                    <div class="calendar-header">
                        <button class="nav-btn">◀</button>
                        <h4>March 2026</h4>
                        <button class="nav-btn">▶</button>
                    </div>
                    <div class="calendar-grid">
                        <div class="cal-day-header">Sun</div><div class="cal-day-header">Mon</div><div class="cal-day-header">Tue</div><div class="cal-day-header">Wed</div><div class="cal-day-header">Thu</div><div class="cal-day-header">Fri</div><div class="cal-day-header">Sat</div>
                        <div class="cal-day"><span>1</span><div class="cal-event">2 Bookings</div></div>
                        <div class="cal-day"><span>2</span><div class="cal-event">1 Booking</div></div>
                        <div class="cal-day"><span>3</span></div>
                        <div class="cal-day"><span>4</span><div class="cal-event">3 Bookings</div></div>
                        <div class="cal-day"><span>5</span><div class="cal-event">VET: 5</div></div>
                        <div class="cal-day"><span>6</span></div>
                        <div class="cal-day"><span>7</span><div class="cal-event">1 Booking</div></div>
                        <div class="cal-day"><span>8</span></div>
                        <div class="cal-day"><span>9</span><div class="cal-event">2 Bookings</div></div>
                        <div class="cal-day"><span>10</span><div class="cal-event">1 Booking</div></div>
                        <div class="cal-day"><span>11</span></div>
                        <div class="cal-day"><span>12</span><div class="cal-event">VET: 8</div></div>
                        <div class="cal-day"><span>13</span></div>
                        <div class="cal-day"><span>14</span></div>
                        <div class="cal-day"><span>15</span><div class="cal-event">Workshop</div></div>
                        <div class="cal-day"><span>16</span></div>
                        <div class="cal-day"><span>17</span><div class="cal-event">1 Booking</div></div>
                        <div class="cal-day"><span>18</span></div>
                        <div class="cal-day"><span>19</span><div class="cal-event">VET: 6</div></div>
                        <div class="cal-day"><span>20</span><div class="cal-event">2 Bookings</div></div>
                        <div class="cal-day"><span>21</span></div>
                        <div class="cal-day"><span>22</span><div class="cal-event">Festival</div></div>
                        <div class="cal-day"><span>23</span></div>
                        <div class="cal-day"><span>24</span></div>
                        <div class="cal-day"><span>25</span></div>
                        <div class="cal-day"><span>26</span><div class="cal-event">VET: 4</div></div>
                        <div class="cal-day"><span>27</span></div>
                        <div class="cal-day"><span>28</span></div>
                        <div class="cal-day"><span>29</span></div>
                        <div class="cal-day"><span>30</span><div class="cal-event">1 Booking</div></div>
                        <div class="cal-day"><span>31</span></div>
                    </div>
                </div>
            </div>
        </div>
    `,

    // ============================================
    // TIER 3 - LMS (LEARNING MANAGEMENT SYSTEM)
    // ============================================
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
            
            <!-- Courses Tab -->
            <div id="lms-courses" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">📚</span>
                        <span class="kpi-val">24</span>
                        <span class="kpi-lbl">Total Courses</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">👥</span>
                        <span class="kpi-val">156</span>
                        <span class="kpi-lbl">Enrolled</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">✅</span>
                        <span class="kpi-val">89</span>
                        <span class="kpi-lbl">Completed</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">⭐</span>
                        <span class="kpi-val">4.5</span>
                        <span class="kpi-lbl">Avg Rating</span>
                    </div>
                </div>
                <div class="course-grid">
                    <div class="course-card">
                        <div class="course-thumb">🌾</div>
                        <h4>Organic Farming Basics</h4>
                        <p>Learn fundamentals of organic farming techniques</p>
                        <div class="course-meta"><span>12 Modules</span><span>4.5★</span></div>
                        <button class="crm-btn">Edit</button>
                    </div>
                    <div class="course-card">
                        <div class="course-thumb">🐄</div>
                        <h4>Cattle Management</h4>
                        <p>Modern dairy farming and cattle care practices</p>
                        <div class="course-meta"><span>8 Modules</span><span>4.8★</span></div>
                        <button class="crm-btn">Edit</button>
                    </div>
                    <div class="course-card">
                        <div class="course-thumb">🔬</div>
                        <h4>Veterinary First Aid</h4>
                        <p>Emergency care for common livestock ailments</p>
                        <div class="course-meta"><span>10 Modules</span><span>4.6★</span></div>
                        <button class="crm-btn">Edit</button>
                    </div>
                    <div class="course-card">
                        <div class="course-thumb">💰</div>
                        <h4>Farm Business Management</h4>
                        <p>Financial planning and marketing for farmers</p>
                        <div class="course-meta"><span>15 Modules</span><span>4.3★</span></div>
                        <button class="crm-btn">Edit</button>
                    </div>
                </div>
            </div>
            
            <!-- My Learning Tab -->
            <div id="lms-my-learning" class="crm-tab-content">
                <h3>📖 My Enrolled Courses</h3>
                <div class="progress-courses">
                    <div class="progress-course">
                        <div class="course-info">
                            <h4>Organic Farming Advanced</h4>
                            <p>Started: Feb 15, 2026 • Due: Mar 15, 2026</p>
                        </div>
                        <div class="progress-bar"><div class="progress-fill" style="width: 65%"></div></div>
                        <span class="progress-text">65% Complete</span>
                        <button class="crm-btn">Continue</button>
                    </div>
                    <div class="progress-course">
                        <div class="course-info">
                            <h4>Cattle Nutrition</h4>
                            <p>Started: Feb 20, 2026 • Due: Mar 20, 2026</p>
                        </div>
                        <div class="progress-bar"><div class="progress-fill" style="width: 40%"></div></div>
                        <span class="progress-text">40% Complete</span>
                        <button class="crm-btn">Continue</button>
                    </div>
                    <div class="progress-course">
                        <div class="course-info">
                            <h4>Agri-Tech Innovations</h4>
                            <p>Started: Mar 01, 2026 • Due: Apr 01, 2026</p>
                        </div>
                        <div class="progress-bar"><div class="progress-fill" style="width: 15%"></div></div>
                        <span class="progress-text">15% Complete</span>
                        <button class="crm-btn">Continue</button>
                    </div>
                </div>
            </div>
            
            <!-- Certifications Tab -->
            <div id="lms-certifications" class="crm-tab-content">
                <h3>🏆 My Certifications</h3>
                <div class="cert-grid">
                    <div class="cert-card">
                        <div class="cert-icon">🎖️</div>
                        <h4>Organic Farming Fundamentals</h4>
                        <p>Issued: Jan 15, 2026</p>
                        <p>Valid until: Jan 15, 2027</p>
                        <button class="crm-btn">View Certificate</button>
                    </div>
                    <div class="cert-card">
                        <div class="cert-icon">🎖️</div>
                        <h4>Dairy Management</h4>
                        <p>Issued: Dec 20, 2025</p>
                        <p>Valid until: Dec 20, 2026</p>
                        <button class="crm-btn">View Certificate</button>
                    </div>
                </div>
            </div>
            
            <!-- Assessments Tab -->
            <div id="lms-assessments" class="crm-tab-content">
                <h3>📝 Assessments & Quizzes</h3>
                <table class="data-table">
                    <thead><tr><th>Assessment</th><th>Course</th><th>Score</th><th>Status</th><th>Date</th></tr></thead>
                    <tbody>
                        <tr><td>Organic Farming Quiz 1</td><td>Organic Farming Basics</td><td>85%</td><td><span class="pill confirmed">Passed</span></td><td>Feb 10, 2026</td></tr>
                        <tr><td>Cattle Health Exam</td><td>Cattle Management</td><td>78%</td><td><span class="pill confirmed">Passed</span></td><td>Feb 18, 2026</td></tr>
                        <tr><td>Farm Economics Test</td><td>Farm Business</td><td>92%</td><td><span class="pill confirmed">Passed</span></td><td>Feb 25, 2026</td></tr>
                        <tr><td>Advanced Organic Quiz</td><td>Organic Farming Advanced</td><td>--</td><td><span class="pill pending">Pending</span></td><td>Due: Mar 15, 2026</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Analytics Tab -->
            <div id="lms-analytics" class="crm-tab-content">
                <h3>📊 Learning Analytics</h3>
                <div class="kpi-row">
                    <div class="kpi-card"><span class="kpi-icon">⏱️</span><span class="kpi-val">24h</span><span class="kpi-lbl">Total Learning Time</span></div>
                    <div class="kpi-card"><span class="kpi-icon">📖</span><span class="kpi-val">18</span><span class="kpi-lbl">Modules Completed</span></div>
                    <div class="kpi-card"><span class="kpi-icon">🏆</span><span class="kpi-val">2</span><span class="kpi-lbl">Certificates Earned</span></div>
                    <div class="kpi-card"><span class="kpi-icon">📈</span><span class="kpi-val">+15%</span><span class="kpi-lbl">This Month</span></div>
                </div>
                <div class="chart-placeholder">
                    <p>📈 Learning Progress Over Time</p>
                    <div class="mock-chart">
                        <div class="bar" style="height: 30%"></div>
                        <div class="bar" style="height: 45%"></div>
                        <div class="bar" style="height: 60%"></div>
                        <div class="bar" style="height: 55%"></div>
                        <div class="bar" style="height: 75%"></div>
                        <div class="bar" style="height: 80%"></div>
                    </div>
                </div>
            </div>
        </div>
    `,

    // ============================================
    // TIER 3 - FIELD SERVICE MODULE
    // ============================================
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
            
            <!-- All Jobs Tab -->
            <div id="fs-all-jobs" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">📋</span>
                        <span class="kpi-val">89</span>
                        <span class="kpi-lbl">Total Jobs</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">⏳</span>
                        <span class="kpi-val">23</span>
                        <span class="kpi-lbl">Pending</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">🔄</span>
                        <span class="kpi-val">12</span>
                        <span class="kpi-lbl">In Progress</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">✅</span>
                        <span class="kpi-val">54</span>
                        <span class="kpi-lbl">Completed</span>
                    </div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Job ID</th><th>Service</th><th>Location</th><th>Farmer</th><th>Assigned To</th><th>Date</th><th>Status</th></tr></thead>
                    <tbody>
                        <tr><td>FS-001</td><td>Soil Testing</td><td>Village: Kuppam</td><td>Ramu</td><td>Field Team A</td><td>Mar 01</td><td><span class="pill pending">Scheduled</span></td></tr>
                        <tr><td>FS-002</td><td>Crop Inspection</td><td>Village: Palamaner</td><td>Lakshman</td><td>Field Team B</td><td>Mar 01</td><td><span class="pill confirmed">In Progress</span></td></tr>
                        <tr><td>FS-003</td><td>Equipment Repair</td><td>Village: Bangarupalem</td><td>Venkatesh</td><td>Tech Team</td><td>Feb 28</td><td><span class="pill confirmed">Completed</span></td></tr>
                        <tr><td>FS-004</td><td>Water Analysis</td><td>Village: Gudipala</td><td>Anil</td><td>Lab Team</td><td>Mar 02</td><td><span class="pill pending">Scheduled</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Scheduled Tab -->
            <div id="fs-scheduled" class="crm-tab-content">
                <h3>📅 Scheduled Field Jobs</h3>
                <div class="schedule-list">
                    <div class="job-card">
                        <div class="job-header">
                            <h4>FS-001: Soil Testing</h4>
                            <span class="pill pending">Scheduled</span>
                        </div>
                        <p>📍 Village: Kuppam, Plot #45</p>
                        <p>👤 Farmer: Ramu Naidu</p>
                        <p>📅 Date: Mar 01, 2026</p>
                        <p>👥 Team: Field Team A (2 members)</p>
                        <button class="crm-btn">Start Job</button>
                    </div>
                    <div class="job-card">
                        <div class="job-header">
                            <h4>FS-004: Water Analysis</h4>
                            <span class="pill pending">Scheduled</span>
                        </div>
                        <p>📍 Village: Gudipala, Borewell #12</p>
                        <p>👤 Farmer: Anil Kumar</p>
                        <p>📅 Date: Mar 02, 2026</p>
                        <p>👥 Team: Lab Team (1 member)</p>
                        <button class="crm-btn">Start Job</button>
                    </div>
                </div>
            </div>
            
            <!-- In Progress Tab -->
            <div id="fs-in-progress" class="crm-tab-content">
                <h3>🔄 Currently Active Jobs</h3>
                <div class="job-card active-job">
                    <div class="job-header">
                        <h4>FS-002: Crop Inspection</h4>
                        <span class="pill confirmed">In Progress</span>
                    </div>
                    <p>📍 Location: Village Palamaner, Block C</p>
                    <p>👤 Farmer: Lakshman Reddy</p>
                    <p>⏱️ Started: 09:30 AM</p>
                    <p>👥 Assigned: Field Team B</p>
                    <div class="job-notes">
                        <p><strong>Notes:</strong> Checking paddy crop for pest infestation. Sample collected.</p>
                    </div>
                    <button class="crm-btn">Update Status</button>
                    <button class="crm-btn">Complete Job</button>
                </div>
            </div>
            
            <!-- Completed Tab -->
            <div id="fs-completed" class="crm-tab-content">
                <h3>✅ Completed Jobs</h3>
                <table class="data-table">
                    <thead><tr><th>Job ID</th><th>Service</th><th>Location</th><th>Completed</th><th>Rating</th></tr></thead>
                    <tbody>
                        <tr><td>FS-003</td><td>Equipment Repair</td><td>Village: Bangarupalem</td><td>Feb 28, 2026</td><td>⭐⭐⭐⭐⭐</td></tr>
                        <tr><td>FS-156</td><td>Soil Testing</td><td>Village: Kuppam</td><td>Feb 27, 2026</td><td>⭐⭐⭐⭐</td></tr>
                        <tr><td>FS-155</td><td>Crop Consultation</td><td>Village: Palamaner</td><td>Feb 26, 2026</td><td>⭐⭐⭐⭐⭐</td></tr>
                        <tr><td>FS-154</td><td>Fertilizer Application</td><td>Village: Gudipala</td><td>Feb 25, 2026</td><td>⭐⭐⭐</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Field Map Tab -->
            <div id="fs-field-map" class="crm-tab-content">
                <h3>🗺️ Field Service Map</h3>
                <div class="map-placeholder">
                    <div class="map-marker" style="top: 20%; left: 30%;"><span class="marker-dot pending"></span><span class="marker-label">FS-001</span></div>
                    <div class="map-marker" style="top: 45%; left: 55%;"><span class="marker-dot active"></span><span class="marker-label">FS-002</span></div>
                    <div class="map-marker" style="top: 70%; left: 40%;"><span class="marker-dot pending"></span><span class="marker-label">FS-004</span></div>
                    <div class="map-legend">
                        <span><span class="marker-dot pending"></span> Scheduled</span>
                        <span><span class="marker-dot active"></span> In Progress</span>
                        <span><span class="marker-dot completed"></span> Completed</span>
                    </div>
                </div>
            </div>
        </div>
    `,

    // ============================================
    // TIER 3 - FARMER PORTAL
    // ============================================
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
            
            <!-- Dashboard Tab -->
            <div id="fp-dashboard" class="crm-tab-content active">
                <div class="welcome-banner">
                    <h3>👋 Welcome back, Farmer!</h3>
                    <p>Last login: Today, 08:30 AM</p>
                </div>
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">🌾</span>
                        <span class="kpi-val">12</span>
                        <span class="kpi-lbl">Acres Cultivated</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">🐄</span>
                        <span class="kpi-val">8</span>
                        <span class="kpi-lbl">Livestock</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">💰</span>
                        <span class="kpi-val">₹2.4L</span>
                        <span class="kpi-lbl">This Season</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">📋</span>
                        <span class="kpi-val">3</span>
                        <span class="kpi-lbl">Pending Tasks</span>
                    </div>
                </div>
                <div class="farmer-alerts">
                    <h4>🔔 Alerts & Notifications</h4>
                    <div class="alert-item"><span class="alert-icon">⚠️</span> Weather Alert: Heavy rain expected on Mar 05</div>
                    <div class="alert-item"><span class="alert-icon">✅</span> Soil test results available for Plot #3</div>
                    <div class="alert-item"><span class="alert-icon">📅</span> Vaccination camp on Mar 10</div>
                </div>
            </div>
            
            <!-- My Crops Tab -->
            <div id="fp-crops" class="crm-tab-content">
                <h3>🌾 My Crops</h3>
                <button class="crm-btn">+ Add Crop</button>
                <div class="crop-grid">
                    <div class="crop-card">
                        <div class="crop-icon">🌾</div>
                        <h4>Paddy (Sona Masuri)</h4>
                        <p>5 Acres • Planting Stage</p>
                        <p>Expected Harvest: Apr 2026</p>
                        <button class="crm-btn">View Details</button>
                    </div>
                    <div class="crop-card">
                        <div class="crop-icon">🌽</div>
                        <h4>Maize</h4>
                        <p>3 Acres • vegetative Stage</p>
                        <p>Expected Harvest: Mar 2026</p>
                        <button class="crm-btn">View Details</button>
                    </div>
                    <div class="crop-card">
                        <div class="crop-icon">🥜</div>
                        <h4>Groundnut</h4>
                        <p>4 Acres • Harvested</p>
                        <p>Yield: 12 quintals/acre</p>
                        <button class="crm-btn">View Details</button>
                    </div>
                </div>
            </div>
            
            <!-- Livestock Tab -->
            <div id="fp-livestock" class="crm-tab-content">
                <h3>🐄 My Livestock</h3>
                <button class="crm-btn">+ Register Animal</button>
                <table class="data-table">
                    <thead><tr><th>ID</th><th>Type</th><th>Breed</th><th>Age</th><th>Health</th><th>Last Checkup</th></tr></thead>
                    <tbody>
                        <tr><td>ANM-001</td><td>Cow</td><td>Holstein</td><td>4 years</td><td><span class="pill confirmed">Healthy</span></td><td>Feb 20, 2026</td></tr>
                        <tr><td>ANM-002</td><td>Buffalo</td><td>Murrah</td><td>5 years</td><td><span class="pill confirmed">Healthy</span></td><td>Feb 20, 2026</td></tr>
                        <tr><td>ANM-003</td><td>Goat</td><td>Telangana Goat</td><td>2 years</td><td><span class="pill pending">Needs Attention</span></td><td>Feb 15, 2026</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Schemes Tab -->
            <div id="fp-schemes" class="crm-tab-content">
                <h3>🏛️ Government Schemes</h3>
                <div class="scheme-list">
                    <div class="scheme-card">
                        <h4>PM-KISAN</h4>
                        <p>Income support of ₹6000/year</p>
                        <p>Status: <span class="pill confirmed">Active</span></p>
                        <button class="crm-btn">View Details</button>
                    </div>
                    <div class="scheme-card">
                        <h4>Fasal Bima Yojana</h4>
                        <p>Crop insurance scheme</p>
                        <p>Status: <span class="pill confirmed">Enrolled</span></p>
                        <button class="crm-btn">Claim Status</button>
                    </div>
                    <div class="scheme-card">
                        <h4>Kisan Credit Card</h4>
                        <p>Easy credit for farmers</p>
                        <p>Status: <span class="pill pending">Applied</span></p>
                        <button class="crm-btn">Track Application</button>
                    </div>
                </div>
            </div>
            
            <!-- Market Prices Tab -->
            <div id="fp-market" class="crm-tab-content">
                <h3>📈 Today's Market Prices</h3>
                <div class="market-ticker">
                    <div class="ticker-item up">🌾 Paddy: ₹2,200/quintal ▲</div>
                    <div class="ticker-item up">🌽 Maize: ₹1,950/quintal ▲</div>
                    <div class="ticker-item down">🥜 Groundnut: ₹5,100/quintal ▼</div>
                    <div class="ticker-item stable">🥛 Milk: ₹28/liter ─</div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Crop</th><th>Yesterday</th><th>Today</th><th>Change</th></tr></thead>
                    <tbody>
                        <tr><td>Paddy (Sona)</td><td>₹2,150</td><td>₹2,200</td><td class="price-up">▲ +2.3%</td></tr>
                        <tr><td>Maize</td><td>₹1,900</td><td>₹1,950</td><td class="price-up">▲ +2.6%</td></tr>
                        <tr><td>Groundnut</td><td>₹5,200</td><td>₹5,100</td><td class="price-down">▼ -1.9%</td></tr>
                        <tr><td>Red Chillies</td><td>₹18,500</td><td>₹18,500</td><td class="price-stable">─ 0%</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    `,

    // ============================================
    // TIER 3 - SURVEY & FEEDBACK MODULE
    // ============================================
    survey: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>📋 Survey & Feedback</h2>
                <button class="crm-btn" onclick="surveyTab('all-surveys', this)">+ Create Survey</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="surveyTab('all-surveys', this)">All Surveys</button>
                <button class="crm-tab-btn" onclick="surveyTab('active', this)">Active</button>
                <button class="crm-tab-btn" onclick="surveyTab('results', this)">Results</button>
                <button class="crm-tab-btn" onclick="surveyTab('feedback', this)">Feedback</button>
            </div>
            
            <!-- All Surveys Tab -->
            <div id="survey-all-surveys" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">📝</span>
                        <span class="kpi-val">15</span>
                        <span class="kpi-lbl">Total Surveys</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">👥</span>
                        <span class="kpi-val">1,234</span>
                        <span class="kpi-lbl">Responses</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">⭐</span>
                        <span class="kpi-val">4.2</span>
                        <span class="kpi-lbl">Avg Rating</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">📈</span>
                        <span class="kpi-val">87%</span>
                        <span class="kpi-lbl">Response Rate</span>
                    </div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Survey</th><th>Type</th><th>Questions</th><th>Responses</th><th>Status</th><th>Created</th></tr></thead>
                    <tbody>
                        <tr><td>Customer Satisfaction</td><td>NPS</td><td>5</td><td>234</td><td><span class="pill confirmed">Active</span></td><td>Feb 20</td></tr>
                        <tr><td>Service Quality</td><td>Rating</td><td>10</td><td>156</td><td><span class="pill confirmed">Active</span></td><td>Feb 18</td></tr>
                        <tr><td>Product Feedback</td><td>Multiple Choice</td><td>15</td><td>89</td><td><span class="pill pending">Draft</span></td><td>--</td></tr>
                        <tr><td>Farmer Training</td><td>Quiz</td><td>20</td><td>445</td><td><span class="pill confirmed">Completed</span></td><td>Jan 15</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Active Tab -->
            <div id="survey-active" class="crm-tab-content">
                <h3>📢 Active Surveys</h3>
                <div class="survey-card">
                    <div class="survey-header">
                        <h4>Customer Satisfaction Survey</h4>
                        <span class="pill confirmed">Active</span>
                    </div>
                    <p>Help us improve our services! Rate your experience.</p>
                    <p>📅 Ends: Mar 31, 2026</p>
                    <p>👥 Target: All Customers</p>
                    <div class="survey-stats">
                        <div class="stat"><span class="stat-val">234</span><span class="stat-lbl">Responses</span></div>
                        <div class="stat"><span class="stat-val">4.3</span><span class="stat-lbl">Avg Score</span></div>
                    </div>
                    <button class="crm-btn">View Results</button>
                    <button class="crm-btn">Close Survey</button>
                </div>
                <div class="survey-card">
                    <div class="survey-header">
                        <h4>Service Quality Rating</h4>
                        <span class="pill confirmed">Active</span>
                    </div>
                    <p>Rate the quality of our field services</p>
                    <p>📅 Ends: Mar 15, 2026</p>
                    <p>👥 Target: Farmers</p>
                    <div class="survey-stats">
                        <div class="stat"><span class="stat-val">156</span><span class="stat-lbl">Responses</span></div>
                        <div class="stat"><span class="stat-val">4.1</span><span class="stat-lbl">Avg Score</span></div>
                    </div>
                    <button class="crm-btn">View Results</button>
                    <button class="crm-btn">Close Survey</button>
                </div>
            </div>
            
            <!-- Results Tab -->
            <div id="survey-results" class="crm-tab-content">
                <h3>📊 Survey Results</h3>
                <div class="result-chart">
                    <h4>How likely are you to recommend us?</h4>
                    <div class="nps-scale">
                        <div class="nps-bar" style="width: 15%"><span>0-3: Detractors</span></div>
                        <div class="nps-bar" style="width: 25%"><span>4-6: Passives</span></div>
                        <div class="nps-bar" style="width: 60%"><span>7-10: Promoters</span></div>
                    </div>
                    <p class="nps-score">NPS Score: <strong>+45</strong></p>
                </div>
                <table class="data-table">
                    <thead><tr><th>Question</th><th>Avg Rating</th><th>Responses</th></tr></thead>
                    <tbody>
                        <tr><td>Overall Satisfaction</td><td>4.3/5</td><td>234</td></tr>
                        <tr><td>Service Quality</td><td>4.1/5</td><td>234</td></tr>
                        <tr><td>Value for Money</td><td>4.4/5</td><td>234</td></tr>
                        <tr><td>Likelihood to Return</td><td>4.2/5</td><td>234</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Feedback Tab -->
            <div id="survey-feedback" class="crm-tab-content">
                <h3>💬 Recent Feedback</h3>
                <div class="feedback-list">
                    <div class="feedback-card">
                        <div class="feedback-header">
                            <span class="feedback-rating">⭐⭐⭐⭐⭐</span>
                            <span class="feedback-date">Feb 28, 2026</span>
                        </div>
                        <p>"Excellent organic produce! Will definitely order again. The vegetables were fresh and well-packed."</p>
                        <p class="feedback-source">- Rajesh Kumar, Customer</p>
                    </div>
                    <div class="feedback-card">
                        <div class="feedback-header">
                            <span class="feedback-rating">⭐⭐⭐⭐</span>
                            <span class="feedback-date">Feb 27, 2026</span>
                        </div>
                        <p>"Good service, but delivery was slightly delayed. Overall satisfied with the quality."</p>
                        <p class="feedback-source">- Priya Sharma, Customer</p>
                    </div>
                    <div class="feedback-card">
                        <div class="feedback-header">
                            <span class="feedback-rating">⭐⭐⭐⭐⭐</span>
                            <span class="feedback-date">Feb 26, 2026</span>
                        </div>
                        <p>"The veterinary service was excellent. Dr. Srinivas was very patient with our cattle."</p>
                        <p class="feedback-source">- Lakshman Reddy, Farmer</p>
                    </div>
                </div>
            </div>
        </div>
    `,

    // ============================================
    // TIER 3 - GOVERNMENT SCHEMES TRACKER
    // ============================================
    schemes: `
        <div class="crm-pn">
            <div class="crm-hdr">
                <h2>🏛️ Government Schemes Tracker</h2>
                <button class="crm-btn" onclick="schemeTab('all-schemes', this)">+ Track Scheme</button>
            </div>
            <div class="crm-tabs">
                <button class="crm-tab-btn active" onclick="schemeTab('all-schemes', this)">All Schemes</button>
                <button class="crm-tab-btn" onclick="schemeTab('applied', this)">Applied</button>
                <button class="crm-tab-btn" onclick="schemeTab('pending', this)">Pending</button>
                <button class="crm-tab-btn" onclick="schemeTab('approved', this)">Approved</button>
                <button class="crm-tab-btn" onclick="schemeTab('rejected', this)">Rejected</button>
            </div>
            
            <!-- All Schemes Tab -->
            <div id="scheme-all-schemes" class="crm-tab-content active">
                <div class="kpi-row">
                    <div class="kpi-card">
                        <span class="kpi-icon">📋</span>
                        <span class="kpi-val">28</span>
                        <span class="kpi-lbl">Total Schemes</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">⏳</span>
                        <span class="kpi-val">8</span>
                        <span class="kpi-lbl">Pending</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">✅</span>
                        <span class="kpi-val">15</span>
                        <span class="kpi-lbl">Approved</span>
                    </div>
                    <div class="kpi-card">
                        <span class="kpi-icon">💰</span>
                        <span class="kpi-val">₹45L</span>
                        <span class="kpi-lbl">Total Benefits</span>
                    </div>
                </div>
                <table class="data-table">
                    <thead><tr><th>Scheme</th><th>Department</th><th>Benefit</th><th>Applied</th><th>Status</th><th>Amount</th></tr></thead>
                    <tbody>
                        <tr><td>PM-KISAN</td><td>Central</td><td>Income Support</td><td>Jan 2025</td><td><span class="pill confirmed">Active</span></td><td>₹6,000/yr</td></tr>
                        <tr><td>Fasal Bima</td><td>Central</td><td>Crop Insurance</td><td>Jun 2025</td><td><span class="pill confirmed">Active</span></td><td>₹2,400/yr</td></tr>
                        <tr><td>KCC</td><td> NABARD</td><td>Credit Card</td><td>Feb 2026</td><td><span class="pill pending">Pending</span></td><td>₹3,00,000</td></tr>
                        <tr><td>Solar Pump</td><td>State</td><td>Subsidy</td><td>Jan 2026</td><td><span class="pill pending">Under Review</span></td><td>₹50,000</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Applied Tab -->
            <div id="scheme-applied" class="crm-tab-content">
                <h3>📝 Applied Schemes</h3>
                <table class="data-table">
                    <thead><tr><th>Scheme</th><th>Applied Date</th><th>Reference No.</th><th>Current Status</th></tr></thead>
                    <tbody>
                        <tr><td>Kisan Credit Card</td><td>Feb 15, 2026</td><td>KCC/2026/001234</td><td><span class="pill pending">Pending</span></td></tr>
                        <tr><td>Solar Pump Subsidy</td><td>Jan 20, 2026</td><td>SP/2026/000567</td><td><span class="pill pending">Under Review</span></td></tr>
                        <tr><td>Cold Storage Grant</td><td>Dec 2025</td><td>CS/2025/000890</td><td><span class="pill pending">Documents Verifying</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Pending Tab -->
            <div id="scheme-pending" class="crm-tab-content">
                <h3>⏳ Pending Approvals</h3>
                <div class="pending-schemes">
                    <div class="scheme-item">
                        <h4>Kisan Credit Card</h4>
                        <p>📅 Applied: Feb 15, 2026</p>
                        <p>📋 Awaiting: Bank Verification</p>
                        <button class="crm-btn">Upload Documents</button>
                    </div>
                    <div class="scheme-item">
                        <h4>Solar Pump Subsidy</h4>
                        <p>📅 Applied: Jan 20, 2026</p>
                        <p>📋 Awaiting: Site Inspection</p>
                        <button class="crm-btn">Schedule Inspection</button>
                    </div>
                </div>
            </div>
            
            <!-- Approved Tab -->
            <div id="scheme-approved" class="crm-tab-content">
                <h3>✅ Approved Schemes</h3>
                <table class="data-table">
                    <thead><tr><th>Scheme</th><th>Approved Date</th><th>Benefit Amount</th><th>Disbursement</th></tr></thead>
                    <tbody>
                        <tr><td>PM-KISAN</td><td>Jan 15, 2025</td><td>₹6,000</td><td><span class="pill confirmed">Received</span></td></tr>
                        <tr><td>Fasal Bima Yojana</td><td>Jun 10, 2025</td><td>₹2,400</td><td><span class="pill confirmed">Active</span></td></tr>
                        <tr><td>Farm Machinery Subsidy</td><td>Mar 2024</td><td>₹75,000</td><td><span class="pill confirmed">Received</span></td></tr>
                        <tr><td>Godown Construction</td><td>Nov 2024</td><td>₹2,50,000</td><td><span class="pill confirmed">Partially Received</span></td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Rejected Tab -->
            <div id="scheme-rejected" class="crm-tab-content">
                <h3>❌ Rejected Applications</h3>
                <table class="data-table">
                    <thead><tr><th>Scheme</th><th>Rejected Date</th><th>Reason</th><th>Appeal</th></tr></thead>
                    <tbody>
                        <tr><td>Drip Irrigation Grant</td><td>Oct 2025</td><td>Land not suitable</td><td><button class="crm-btn">Appeal</button></td></tr>
                        <tr><td>Warehouse Subsidy</td><td>Aug 2025</td><td>Already availed similar benefit</td><td><button class="crm-btn">View Details</button></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    `,'''
    
    # Find where to insert - before the last closing of pages object
    # Look for the last page template closing
    if "    // ============================================\n    // TIER 2" in content:
        # Insert before Tier 2 (we're adding Tier 3)
        insert_pos = content.find("    // ============================================\n    // TIER 2")
    else:
        # Try to find other landmarks
        insert_pos = content.rfind("};")
    
    if insert_pos > 0:
        content = content[:insert_pos] + tier3_pages + "\n" + content[insert_pos:]
        
        with open('dashboard/app.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Tier 3 modules injected successfully!")
    else:
        print("⚠️ Could not find insertion point")

if __name__ == "__main__":
    inject_tier3_modules()
