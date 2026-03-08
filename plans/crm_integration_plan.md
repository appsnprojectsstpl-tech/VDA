# CRM Integration Plan for Vedavathi Dashboard

## Overview
Add complete CRM functionality to the existing dashboard with: contacts, leads, deals pipeline, tasks, communications, and analytics.

## Database Schema (PostgreSQL/InsForge)

### Core Tables
- `crm_contacts` - Customer database
- `crm_leads` - Lead tracking
- `crm_deals` - Sales pipeline
- `crm_pipeline_stages` - Pipeline configuration
- `crm_tasks` - Task management
- `crm_communications` - Emails, calls, notes
- `crm_activities` - Activity history
- `crm_users` - User management
- `crm_roles` - Role definitions

### API Endpoints
```
Contacts:  GET/POST/PUT/DELETE /api/crm/contacts
Leads:    GET/POST/PUT/DELETE /api/crm/leads
Deals:    GET/POST/PUT/DELETE /api/crm/deals
Tasks:    GET/POST/PUT/DELETE /api/crm/tasks
Comms:    GET/POST /api/crm/communications
Analytics: GET /api/crm/analytics/*
```

## Frontend Modules

### Tabs Required
1. Contacts - Table with search/filter
2. Leads - List with status tracking
3. Pipeline - Kanban board
4. Tasks - Task list with assignees
5. Communications - Activity feed
6. Analytics - Charts and KPIs

## Implementation Priority
1. Database schema
2. API endpoints
3. Frontend module shell
4. Contacts tab
5. Leads tab
6. Pipeline tab
7. Tasks tab
8. Communications tab
9. Analytics tab
