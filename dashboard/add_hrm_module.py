#!/usr/bin/env python3
"""
Script to add HRM/Payroll module to app.js
"""

# Read the app.js file
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# HRM module template
hrm_module = '''
    hrm: `
    <div class="page-header"><div class="page-title">👥 HRM & Payroll</div><div class="page-subtitle">247 Employees · ₹1.2 Cr Monthly Payroll · 98% Attendance</div></div>
   <div class="crm-nav">
     <button type="button"  class="crm-tab-btn active"onclick="hrmTab('employees',this)">👨‍💼 Employees</button>
     <button type="button"  class="crm-tab-btn"onclick="hrmTab('attendance',this)">📅 Attendance</button>
     <button type="button"  class="crm-tab-btn"onclick="hrmTab('payroll',this)">💰 Payroll</button>
     <button type="button"  class="crm-tab-btn"onclick="hrmTab('leaves',this)">🏖️ Leaves</button>
     <button type="button"  class="crm-tab-btn"onclick="hrmTab('hreports',this)">📊 Reports</button>
    </div>

    <!-- EMPLOYEES TAB -->
    <div class="crm-pn active"id="hrm-employees">
        <div class="card"><div class="card-title">👨‍💼 Employee Registry</div>
        <div style="margin-bottom:15px;display:flex;gap:10px;">
            <button type="button" class="clean-btn" onclick="showAddEmployeeForm()">➕ Add Employee</button>
            <input type="text" placeholder="Search employees..." style="padding:8px;border:1px solid #ddd;border-radius:4px;">
        </div>
      <table class="data-table">
          <tr><th>ID</th><th>Name</th><th>Designation</th><th>Department</th><th>Zone</th><th>Join Date</th><th>Status</th><th>Actions</th></tr>
          <tr><td>EMP001</td><td>Rajesh Kumar</td><td>Farm Manager</td><td>Agriculture</td><td>Bellary</td><td>2022-01-15</td><td><span class="pill pill-green">Active</span></td><td><button>View</button></td></tr>
          <tr><td>EMP002</td><td>Lakshmi Devi</td><td>Veterinarian</td><td>Veterinary</td><td>Kurnool</td><td>2021-06-01</td><td><span class="pill pill-green">Active</span></td><td><button>View</button></td></tr>
          <tr><td>EMP003</td><td>Mahendra Singh</td><td>Solar Technician</td><td>Energy</td><td>Hyderabad</td><td>2023-03-20</td><td><span class="pill pill-green">Active</span></td><td><button>View</button></td></tr>
          <tr><td>EMP004</td><td>Sunita Rao</td><td>Dairy Supervisor</td><td>Dairy</td><td>Gadwal</td><td>2020-11-10</td><td><span class="pill pill-green">Active</span></td><td><button>View</button></td></tr>
          <tr><td>EMP005</td><td>Prakash Reddy</td><td>Logistics Coordinator</td><td>Operations</td><td>Bellary</td><td>2024-02-01</td><td><span class="pill pill-amber">Probation</span></td><td><button>View</button></td></tr>
          <tr><td>EMP006</td><td>Anita Devi</td><td>Accounts Manager</td><td>Finance</td><td>Hyderabad</td><td>2021-09-15</td><td><span class="pill pill-green">Active</span></td><td><button>View</button></td></tr>
      </table></div>
    </div>

    <!-- ATTENDANCE TAB -->
    <div class="crm-pn"id="hrm-attendance">
        <div class="card"><div class="card-title">📅 Attendance Tracker</div>
        <div style="display:flex;gap:15px;margin-bottom:15px;">
            <div><strong>Date:</strong> <input type="date" value="2026-02-28"></div>
            <div><strong>Zone:</strong> 
                <select><option>All Zones</option><option>Bellary</option><option>Kurnool</option><option>Gadwal</option><option>Hyderabad</option></select>
            </div>
            <button type="button" class="clean-btn">📥 Export</button>
        </div>
      <table class="data-table">
          <tr><th>Employee</th><th>Department</th><th>Check In</th><th>Check Out</th><th>Hours</th><th>Status</th><th>Remarks</th></tr>
          <tr><td>Rajesh Kumar</td><td>Agriculture</td><td>06:00 AM</td><td>02:00 PM</td><td>8.0</td><td><span class="pill pill-green">Present</span></td><td>-</td></tr>
          <tr><td>Lakshmi Devi</td><td>Veterinary</td><td>08:30 AM</td><td>05:30 PM</td><td>8.0</td><td><span class="pill pill-green">Present</span></td><td>-</td></tr>
          <tr><td>Mahendra Singh</td><td>Energy</td><td>07:00 AM</td><td>-</td><td>-</td><td><span class="pill pill-amber">On Duty</span></td><td>Site visit</td></tr>
          <tr><td>Sunita Rao</td><td>Dairy</td><td>05:30 AM</td><td>01:30 PM</td><td>8.0</td><td><span class="pill pill-green">Present</span></td><td>Early shift</td></tr>
          <tr><td>Prakash Reddy</td><td>Operations</td><td>-</td><td>-</td><td>-</td><td><span class="pill pill-red">Absent</span></td><td>Leave applied</td></tr>
      </table></div>
    </div>

    <!-- PAYROLL TAB -->
    <div class="crm-pn"id="hrm-payroll">
        <div class="card"><div class="card-title">💰 Payroll Processing - February 2026</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <button type="button" class="clean-btn">📥 Download Payslips</button>
            <button type="button" class="clean-btn">🖨️ Print All</button>
            <button type="button" class="clean-btn">📧 Email Payslips</button>
        </div>
      <table class="data-table">
          <tr><th>Employee</th><th>Designation</th><th>Basic Salary</th><th>Allowances</th><th>Deductions</th><th>Net Pay</th><th>Status</th></tr>
          <tr><td>Rajesh Kumar</td><td>Farm Manager</td><td>₹45,000</td><td>₹12,000</td><td>₹5,500</td><td>₹51,500</td><td><span class="pill pill-green">Processed</span></td></tr>
          <tr><td>Lakshmi Devi</td><td>Veterinarian</td><td>₹55,000</td><td>₹15,000</td><td>₹7,200</td><td>₹62,800</td><td><span class="pill pill-green">Processed</span></td></tr>
          <tr><td>Mahendra Singh</td><td>Solar Technician</td><td>₹28,000</td><td>₹8,000</td><td>₹3,200</td><td>₹32,800</td><td><span class="pill pill-green">Processed</span></td></tr>
          <tr><td>Sunita Rao</td><td>Dairy Supervisor</td><td>₹24,000</td><td>₹6,000</td><td>₹2,400</td><td>₹27,600</td><td><span class="pill pill-green">Processed</span></td></tr>
          <tr><td>Prakash Reddy</td><td>Logistics Coordinator</td><td>₹22,000</td><td>₹5,000</td><td>₹2,000</td><td>₹25,000</td><td><span class="pill pill-amber">Pending</span></td></tr>
      </table>
      <div style="margin-top:20px;padding:15px;background:var(--panel-bg);border-radius:8px;">
        <div style="display:flex;justify-content:space-between;"><span><strong>Total Payroll:</strong></span><span>₹12,45,000</span></div>
        <div style="display:flex;justify-content:space-between;"><span><strong>Total Employees:</strong></span><span>247</span></div>
        <div style="display:flex;justify-content:space-between;"><span><strong>Average Salary:</strong></span><span>₹50,404</span></div>
      </div></div>
    </div>

    <!-- LEAVES TAB -->
    <div class="crm-pn"id="hrm-leaves">
        <div class="card"><div class="card-title">🏖️ Leave Management</div>
        <div style="display:flex;gap:10px;margin-bottom:15px;">
            <button type="button" class="clean-btn" onclick="showLeaveRequestForm()">📝 Request Leave</button>
            <button type="button" class="clean-btn">📊 Leave Balance</button>
        </div>
      <table class="data-table">
          <tr><th>Employee</th><th>Leave Type</th><th>From Date</th><th>To Date</th><th>Days</th><th>Reason</th><th>Status</th><th>Actions</th></tr>
          <tr><td>Prakash Reddy</td><td>Sick Leave</td><td>2026-02-28</td><td>2026-02-28</td><td>1</td><td>Medical appointment</td><td><span class="pill pill-green">Approved</span></td><td><button>View</button></td></tr>
          <tr><td>Anita Devi</td><td>Casual Leave</td><td>2026-03-05</td><td>2026-03-07</td><td>3</td><td>Family function</td><td><span class="pill pill-amber">Pending</span></td><td><button>Approve</button></td></tr>
          <tr><td>Rajesh Kumar</td><td>Annual Leave</td><td>2026-04-01</td><td>2026-04-10</td><td>10</td><td>Vacation</td><td><span class="pill pill-amber">Pending</span></td><td><button>Approve</button></td></tr>
          <tr><td>Mahendra Singh</td><td>Comp Off</td><td>2026-03-15</td><td>2026-03-15</td><td>1</td><td>Weekend duty</td><td><span class="pill pill-green">Approved</span></td><td><button>View</button></td></tr>
      </table></div>
    </div>

    <!-- REPORTS TAB -->
    <div class="crm-pn"id="hrm-hreports">
        <div class="card"><div class="card-title">📊 HR Reports & Analytics</div>
        <div class="kpi-grid">
            <div class="kpi-card teal"><div class="kpi-top"><div class="kpi-icon">👥</div></div><div><div class="kpi-value">247</div><div class="kpi-label">Total Employees</div></div></div>
            <div class="kpi-card green"><div class="kpi-top"><div class="kpi-icon">✅</div></div><div><div class="kpi-value">98%</div><div class="kpi-label">Attendance Rate</div></div></div>
            <div class="kpi-card emerald"><div class="kpi-top"><div class="kpi-icon">💰</div></div><div><div class="kpi-value">₹12.4L</div><div class="kpi-label">Monthly Payroll</div></div></div>
            <div class="kpi-card orange"><div class="kpi-top"><div class="kpi-icon">🏖️</div></div><div><div class="kpi-value">12</div><div class="kpi-label">Pending Leaves</div></div></div>
        </div>
    </div>

    `,
'''

# Add HRM module before finance module
old_finance = '''    finance: `
    <div class="page-header">'''

content = content.replace(old_finance, hrm_module + old_finance)

# Write the modified content back
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("HRM module added successfully!")
