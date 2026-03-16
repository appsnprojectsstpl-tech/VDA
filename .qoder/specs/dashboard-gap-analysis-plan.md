# Vedavathi Dashboard - Gap Analysis & Implementation Plan

## Context

The Vedavathi Operations Command Center is a 36-module enterprise ERP dashboard built with vanilla JavaScript. While the **UI structure is comprehensive** (navigation, page templates for all 36 modules, dark theme, accessibility) and the **database layer is complete** (`add_db_integration.js` has CRUD + analytics for all modules), the application is non-functional because:

1. The InsForge backend is disconnected (empty credentials in insforge-config.js)
2. ~50+ onclick handlers are stubs (`alert('Coming soon')`)
3. 8+ ERP modules have "Module under development" placeholders
4. Chart.js is loaded but no charts are rendered
5. No modal forms exist for data entry
6. Tier 3 modules (Field Service, LMS, Survey, Farmer Portal, Schemes) have minimal/stub templates

**Scope**: All 36 modules, full implementation. Auth is deferred (skip for now).

---

## Phase 0: Backend Connection & Data Seeding (CRITICAL)

### 0A. Connect InsForge Backend
**File**: `dashboard/insforge-config.js`
- Use `get-backend-metadata` MCP tool to retrieve backend URL and anon key
- Set `SUPABASE_URL` and `SUPABASE_KEY` with the retrieved credentials
- The existing `window.insforge.fetch/insert/query` code is already correct - only empty credentials prevent data flow
- Verify connection: `hasValidCredentials` check (line 22) must pass, `checkBackendHealth()` should log "Backend connected"

### 0B. Execute Database Schema
**File**: `dashboard/setup_database.sql`
- Run full SQL file against InsForge backend using `run-raw-sql` MCP tool
- Creates ~80 tables across all 36 modules (tourism_bookings, cattle_animals, crm_leads, hrm_employees, inv_products, fin_invoices, etc.)
- If tables already exist, the `CREATE TABLE IF NOT EXISTS` guards will prevent errors

### 0C. Seed Demo Data
- Insert realistic sample data into all tables so the UI shows meaningful content
- Match field names expected by `add_db_integration.js` functions
- Use data consistent with existing hardcoded sample data (employee names, inventory items, KPI values)
- Cover all modules: energy readings, cattle/poultry records, CRM leads, HRM employees, inventory products, finance invoices, etc.

---

## Phase 1: Missing Tab Switchers

**File**: `dashboard/app.js`

8 ERP modules reference tab functions that don't exist. Define them:

| Function | Module | Tab pane class | ID prefix |
|----------|--------|----------------|-----------|
| `crmTab(id, btn)` | CRM & Contracts | `.crm-pn` | `crm-` |
| `hrmTab(id, btn)` | HRM & Payroll | `.crm-pn` | `hrm-` |
| `invTab(id, btn)` | Inventory | `.crm-pn` | `inv-` |
| `finTab(id, btn)` | Finance & Accts | `.crm-pn` | `fin-` |
| `dmsTab(id, btn)` | Documents | `.crm-pn` | `dms-` |
| `wfTab(id, btn)` | Workflow | `.crm-pn` | `wf-` |
| `ticketTab(id, btn)` | Helpdesk | `.crm-pn` | `tick-` |
| `biTab(id, btn)` | BI & Analytics | `.crm-pn` | `bi-` |

Also add Tier 3 module tab switchers if missing: `bookingTab()`, `fpTab()`, `fsTab()`, `lmsTab()`, `surveyTab()`, `schemeTab()`

Each function: scope pane queries to current page container only, expose on `window`.

**Note**: `finTab` is monkey-patched at line ~16325 - define base function before that IIFE.

---

## Phase 2: Modal Form System & CRUD Wiring

### 2A. Build Reusable Modal System
**Files**: `dashboard/app.js`, `dashboard/index.html`, `dashboard/index.css`

Create `ModalManager`:
- `ModalManager.open({ title, fields[], onSubmit })` - generates modal overlay + form dynamically
- `ModalManager.close()` - hides modal
- Add generic modal container `<div id="generic-modal-overlay">` to index.html
- Add modal styles to index.css following existing dark theme (reference `breed-modal-overlay` patterns)

### 2B. Wire Form Functions
**File**: `dashboard/app.js`

Replace stub functions with real ModalManager calls:

| Function | Modal Fields | DB Call |
|----------|-------------|---------|
| `showAddLeadForm()` | Name, Email, Phone, Company, Source, Status, Notes | `db.crm.addLead()` |
| `showAddEmployeeForm()` | First Name, Last Name, ID, Email, Dept, Zone, Salary, Join Date | `db.hrm.addEmployee()` |
| `showLeaveRequestForm()` | Employee, Leave Type, From, To, Reason | `db.hrm.applyLeave()` |
| `showAddItemForm()` | Code, Name, Category, Zone, Stock, Unit, Min Level, Cost | `db.inventory.addProduct()` |
| `showCreatePOForm()` | Vendor, Items, Qty, Value, Delivery Date | `db.inventory.createPO()` |
| `showCreateInvoice()` | Customer, Amount, Invoice Date, Due Date, Items | `db.finance.createInvoice()` |

Each: open modal -> validate -> call DB -> show toast -> refresh page content.

### 2C. Wire Additional Buttons
- "Export PDF/Excel" buttons: implement CSV via existing `VedavathiAPI.export.toCSV()`, add jsPDF CDN for PDF
- Search inputs across modules: `oninput` handler to filter table rows
- "View" buttons on rows: open read-only detail modal
- "Approve/Reject" on workflow items: call `db.workflow.updateStatus()`

---

## Phase 3: Complete CRM Module

**File**: `dashboard/app.js` (modify `crm:` template, lines 3565-3900)

Current state: 8 tab panes all showing "Module under development" placeholder.

Replace each pane's content:

1. **Dashboard** (`crm-dash`): KPI grid (Leads, Contracts, Pipeline Value, Conversion Rate) loaded from `db.crm.getLeadAnalytics()` + `getSalesPipeline()`
2. **Buyers** (`crm-buyers`): Data table loaded from `db.crm.getLeads()` with buyer filter + "Add Buyer" button
3. **Contracts** (`crm-contracts`): Data table from `db.crm.getContracts()` + "Create Contract" modal
4. **Pipeline** (`crm-pipeline`): Visual horizontal pipeline bars from `db.crm.getSalesPipeline()` (New -> Qualified -> Proposal -> Won)
5. **Leads** (`crm-leads`): Data table + "Add Lead" button (already wired to `showAddLeadForm()`)
6. **Tasks** (`crm-tasks`): Task list with filter buttons (already wired to `filterTasks()`)
7. **Communications** (`crm-communications`): Comm log from `db.crm.getCommunications()`
8. **Reports** (`crm-crep`): Summary KPIs + CSS bar charts

Also fix: Remove duplicate tab buttons (leads/tasks appear twice in nav).

---

## Phase 4: Complete HRM, Inventory, Finance Modules

### 4A. HRM Module
**File**: `dashboard/app.js` (modify `hrm:` template, lines 10492-10590)

- Add `initHRM()` function called on page load: loads employees, attendance, payroll from `db.hrm.*`
- Wire "Add Employee" button -> `showAddEmployeeForm()`
- Wire attendance date picker -> load attendance for that date
- Wire "Approve" on leave requests -> `db.workflow.updateStatus()`
- Wire payroll export buttons -> CSV/PDF export

### 4B. Inventory Module
**File**: `dashboard/app.js` (modify `inventory:` template, lines 10592-10679)

- Add `initInventory()` function: loads products, reorder alerts, POs from `db.inventory.*`
- Wire search input + zone selector to filter stock table
- Wire "Add Item" -> `showAddItemForm()`
- Wire "Create PO" -> `showCreatePOForm()` pre-filled with reorder item data

### 4C. Finance Module
**File**: `dashboard/app.js` (modify `finance2:` template, lines 10681-10749)

- Fix HTML typo: line 10703 `<thDue Date</th>` -> `<th>Due Date</th>`
- Add `initFinance()` function: loads summary, invoices, expenses from `db.finance.*`
- Wire "Create Invoice" -> `showCreateInvoice()`
- Add "New Expense" button + modal -> `db.finance.addExpense()`
- Connect existing `loadLiveFinanceDash()` function (line ~16260) to run on page load

---

## Phase 5: Chart.js Integration

**File**: `dashboard/app.js`

Chart.js is loaded (CDN, index.html line 19) but unused. Create `ChartHelper.create(canvasId, type, data, options)` wrapper.

Add charts to:
- **Overview page**: Revenue bar chart, energy trend line, livestock pie chart
- **Finance module**: Revenue vs expenses line chart, expense breakdown doughnut
- **BI & Analytics**: Revenue by zone bar chart, operations radar chart
- **Energy modules**: Power generation time series (existing `<canvas id="sgFlowChart">` + `finance-module-chart`)
- **CRM Pipeline**: Funnel/horizontal stacked bar for lead stages

---

## Phase 6: Stub Modules - Fill Content

### 6A. Helpdesk/Ticketing (line ~10873)
All 4 panes show "Module under development". Build:
- All/Open/My Tickets data tables from `db.ticketing.getTickets()`
- "New Ticket" form: Subject, Category, Priority, Description
- KPI row: Open, In Progress, Resolved, Avg Resolution Time

### 6B. Workflow & Approvals (line ~10825)
Template has good hardcoded data. Wire to real data:
- Load from `db.workflow.getApprovals('pending')`
- Wire Approve/Review buttons

### 6C. DMS - Document Management (line ~10751)
Has browse skeleton. Build:
- Browse: load from `db.dms.getDocuments()`, group by category
- Upload: file upload via InsForge Storage SDK + metadata to `dms_documents`
- Search: `db.dms.searchDocuments(query)`

### 6D. BI & Analytics (line ~10969)
Replace CSS bars with Chart.js charts, load from `db.bi.getCrossModuleSummary()`

### 6E. Tier 3 Modules (Field Service, LMS, Survey, Farmer Portal, Schemes)
Build templates from scratch following `.crm-nav` / `.crm-pn` pattern:
- Each: tabbed interface, KPI cards, data table, basic CRUD forms
- DB layer already exists: `window.dbFieldService`, `window.dbLMS`, `window.dbSurvey`, `window.dbFarmer`, `window.dbSchemes`

---

## Phase 7: Data Export & Real-time

### 7A. Data Export
- CSV: wire existing `VedavathiAPI.export.toCSV()` to all Export buttons across every module
- PDF: add jsPDF via CDN, create `PDFExporter` utility that takes a table element and renders to PDF
- Excel: add SheetJS (xlsx) via CDN for Excel export
- Wire all "Export PDF", "Export Excel", "Download" buttons in all 36 modules

### 7B. Real-time Subscriptions
- Add `window.insforge.subscribe(table, callback)` using InsForge WebSocket
- Subscribe to critical tables: `grid_alerts`, `command_incidents`, `workflow_approvals`
- On new record, show push notification + update active page if relevant

---

## Phase 8: UI/UX Polish

- Replace timeout-based empty state hack with proper loading indicators (skeleton screens)
- Wire global search (`#globalSearch`) to command-palette style module search
- Wire sidebar search (`#sidebarSearch`) to filter menu items
- Ensure responsive tab overflow with horizontal scrolling on all nav bars
- Fix any remaining HTML/CSS inconsistencies

---

## Key Files to Modify

| File | Changes |
|------|---------|
| `dashboard/insforge-config.js` | Backend credentials, real-time subscriptions |
| `dashboard/app.js` | Tab switchers, modal system, form handlers, page init functions, chart rendering, module templates |
| `dashboard/index.html` | Generic modal container, additional CDN imports (jsPDF, SheetJS) |
| `dashboard/index.css` | Modal styles, chart container styles, responsive fixes |
| `dashboard/add_db_integration.js` | Minor additions for update/delete ops if needed |
| `dashboard/api_wrapper.js` | No changes needed (already well-structured) |

---

## Verification Plan

After each phase:
1. Run `node --check dashboard/app.js` for syntax validation
2. Open dashboard in browser (via `node dashboard/server.js` or directly open `dashboard/index.html`)
3. Click through all 36 sidebar menu items - verify page renders without console errors
4. Click all tabs within each module - verify tab switching works
5. Test CRUD: add a record via modal form, verify it appears in table and persists in backend
6. Check browser console for JavaScript errors (no undefined function errors)
7. Test on mobile viewport (Chrome DevTools) for responsive layout

---

## Dependency Order

```
Phase 0 (Backend Connection + Seed Data) -- required first
  |
  +--> Phase 1 (Tab Switchers) -- can start immediately, no backend dependency
  |
  +--> Phase 2 (Modal System) -- requires Phase 0 for DB calls to work
         |
         +--> Phase 3 (CRM) + Phase 4 (HRM/Inv/Fin) -- require Phase 2 modals
                |
                +--> Phase 5 (Charts) -- can overlap with Phase 3/4
                |
                +--> Phase 6 (Stub Modules) -- require Phase 2 patterns
                       |
                       +--> Phase 7 (Export/Realtime) + Phase 8 (Polish)
```
