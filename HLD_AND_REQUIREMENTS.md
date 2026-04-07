# High Level Design (HLD) and Requirements

## Vaishnavi Silks Kanapuraka - Payment Reminder System

**Version:** 1.0  
**Date:** April 2026  
**Business:** Payment tracking and reminder system for MSME saree shop

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Business Requirements](#business-requirements)
3. [Use Cases](#use-cases)
4. [System Overview](#system-overview)
5. [Functional Requirements](#functional-requirements)
6. [Non-Functional Requirements](#non-functional-requirements)
7. [High Level Architecture](#high-level-architecture)
8. [Data Model](#data-model)
9. [User Interface Design](#user-interface-design)
10. [Integration Points](#integration-points)

---

## 1. Executive Summary

### 1.1 Business Problem
Vaishnavi Silks Kanapuraka operates a monthly payment scheme where customers pay installments for sarees. Manual tracking leads to missed payments, poor cash flow, and customer relationship issues.

### 1.2 Solution
A mobile-friendly web application that automates customer payment tracking and sends automated WhatsApp reminders for pending payments.

### 1.3 Business Impact
- **Improved Cash Flow**: Automated reminders reduce payment delays
- **Time Savings**: Eliminate manual tracking and follow-ups
- **Better Customer Relationships**: Professional, timely reminders
- **Scalability**: Handle 100+ customers efficiently

### 1.4 Key Metrics
- 100+ active customers
- Monthly payment amounts: ₹1,000 - ₹5,000
- Collection efficiency target: 90%+ on-time payments
- Average scheme duration: 12 months

---

## 2. Business Requirements

### 2.1 Target Users
- **Primary**: Shop owner and staff
- **Secondary**: Customers (receive reminders)
- **Scale**: Single shop, 1-3 users

### 2.2 Business Model
- **Payment Scheme**: Customers pay fixed monthly amounts
- **Duration**: 6-12 months typically
- **Benefit**: Discount or product at completion
- **Follow-up**: Manual reminders currently, automated via WhatsApp

### 2.3 Current Pain Points
1. **Manual Tracking**: Using notebooks/Excel sheets
2. **Memory Dependent**: Difficult to remember payment status
3. **Time Consuming**: Manual phone calls for reminders
4. **Inconsistent Follow-up**: Some customers forgotten
5. **No Historical Data**: Difficult to analyze payment patterns

### 2.4 Success Criteria
- ✅ Reduce manual tracking time by 80%
- ✅ Improve on-time payment rate to 90%+
- ✅ Zero missed reminders
- ✅ Accessible from mobile devices
- ✅ Simple enough for non-technical users

---

## 3. Use Cases

### 3.1 Primary Use Cases

#### UC-01: Add New Customer
**Actor**: Shop Owner  
**Goal**: Register a new customer in monthly payment scheme  
**Precondition**: User is logged in  
**Flow**:
1. Navigate to "Add Customer" screen
2. Enter customer details (name, phone, amount, duration)
3. System validates phone number (allows duplicates for family members)
4. System auto-generates 12 monthly payment records
5. Customer is added to active customers list

**Success**: Customer added, payments scheduled  
**Alternative**: Validation error shown, user corrects data

---

#### UC-02: Mark Payment as Paid
**Actor**: Shop Owner  
**Goal**: Record customer payment  
**Precondition**: Customer exists, payment is pending  
**Flow**:
1. View customer details or payments screen
2. Select pending payment for current month
3. Click "Mark Paid" button
4. System records payment date and updates status
5. Dashboard statistics update automatically

**Success**: Payment marked paid, collections updated  
**Alternative**: Payment already paid - show message

---

#### UC-03: Send Payment Reminder
**Actor**: Shop Owner  
**Goal**: Remind customer about pending payment  
**Precondition**: Customer has pending payment, joined WhatsApp sandbox  
**Flow**:
1. View dashboard pending payments OR customer details
2. Click "🔔 Reminder" button
3. System formats personalized WhatsApp message
4. Twilio sends message to customer
5. Button shows "✅ Sent Today" and disables
6. Status persists for entire day

**Success**: WhatsApp reminder sent successfully  
**Alternative**: Customer not on sandbox - error logged, manual follow-up needed

---

#### UC-04: View Dashboard
**Actor**: Shop Owner  
**Goal**: Monitor business performance  
**Precondition**: User is logged in  
**Flow**:
1. User logs in to system
2. Dashboard loads automatically
3. Statistics displayed:
   - Total active customers
   - Current month paid count
   - Current month pending count
   - Total collection (current month)
4. Today's pending follow-ups list shown
5. Quick action buttons displayed

**Success**: Complete business overview visible  
**Post-condition**: User can navigate to detailed screens

---

#### UC-05: View Monthly Collections
**Actor**: Shop Owner  
**Goal**: Analyze collection trends  
**Precondition**: User is logged in, payments exist  
**Flow**:
1. Click "📊 Monthly Collections" from dashboard
2. System aggregates all paid payments by month
3. Display list showing:
   - Month and Year (e.g., "Apr 2026")
   - Total amount collected
   - Number of payments
   - Number of unique customers
4. Grand total displayed at top

**Success**: Historical collection data visible  
**Analysis**: Identify seasonal trends, growth patterns

---

### 3.2 Secondary Use Cases

#### UC-06: Search Customer
**Actor**: Shop Owner  
**Goal**: Quickly find customer information  
**Flow**:
1. Navigate to customers screen
2. Type in search box (name or phone)
3. Real-time filtering as user types
4. Click customer to view details

---

#### UC-07: Filter Payments
**Actor**: Shop Owner  
**Goal**: View payments by status or month  
**Flow**:
1. Navigate to payments screen
2. Select month filter (Current/All Months)
3. Select status filter (All/Paid/Pending)
4. System displays matching payments
5. If "All Months + Pending" selected, shows all historical pending

---

#### UC-08: Delete Customer
**Actor**: Shop Owner  
**Goal**: Remove inactive/cancelled customer  
**Precondition**: Customer exists  
**Flow**:
1. View customer details
2. Click "🗑️ Delete Customer" button
3. Confirmation dialog appears
4. User confirms deletion
5. Customer soft-deleted (is_active = false)
6. Removed from active customer lists

**Success**: Customer deactivated, not deleted permanently  
**Note**: Data retained for historical records

---

#### UC-09: Revert Paid Payment
**Actor**: Shop Owner  
**Goal**: Correct accidental payment marking  
**Precondition**: Payment marked as paid incorrectly  
**Flow**:
1. View payment history
2. Find incorrectly marked payment
3. Click "↩ Revert to Unpaid" button
4. System clears paid_date and sets is_paid = false
5. Collections statistics updated

---

### 3.3 System Use Cases

#### UC-10: Automated Daily Reminders
**Actor**: System (Scheduler)  
**Goal**: Send automated reminders to overdue customers  
**Schedule**: Daily at 9:00 AM  
**Flow**:
1. System checks all pending payments with due_date ≤ today
2. Categorizes by days overdue:
   - 0 days: Due today reminder
   - 5 days: First reminder
   - 10 days: Second reminder
   - 15+ days: Final reminder / weekly
3. For each customer, formats appropriate message
4. Sends WhatsApp message via Twilio
5. Logs reminder status

**Success**: All eligible customers reminded  
**Error Handling**: Failed messages logged for manual follow-up

---

## 4. System Overview

### 4.1 System Purpose
A lightweight, mobile-first web application for managing customer payment schemes with automated WhatsApp reminders.

### 4.2 System Scope

**In Scope**:
- Customer registration and management
- Payment tracking and marking
- Dashboard and reporting
- WhatsApp reminder automation
- Monthly collection analytics
- Search and filtering
- Mobile-responsive UI

**Out of Scope** (Future Enhancements):
- Multi-shop management
- Role-based access control
- Advanced analytics and reports
- Integration with accounting software
- Mobile native applications
- Payment gateway integration
- Customer portal/app

### 4.3 Technology Stack

**Backend**:
- FastAPI 0.109.0 (Python web framework)
- SQLAlchemy 2.0.25 (ORM)
- SQLite (Database)
- Pydantic (Data validation)
- APScheduler 3.10.4 (Task scheduling)

**Frontend**:
- Vanilla JavaScript (No framework)
- HTML5 + CSS3
- Mobile-first responsive design
- Fetch API for REST calls

**Integration**:
- Twilio WhatsApp API 8.10.0
- JWT Authentication (python-jose)

**Environment**:
- Python 3.11+
- Windows development environment
- Uvicorn ASGI server

---

## 5. Functional Requirements

### 5.1 Authentication & Security

**FR-1.1**: System shall provide username/password authentication  
**FR-1.2**: System shall use JWT tokens for session management (24-hour expiry)  
**FR-1.3**: Passwords shall be hashed using bcrypt  
**FR-1.4**: All API endpoints except login/register shall require authentication  
**FR-1.5**: System shall provide logout functionality

### 5.2 Customer Management

**FR-2.1**: System shall allow adding customers with: name, phone, monthly_amount, start_date, duration_months  
**FR-2.2**: System shall allow duplicate phone numbers (family members)  
**FR-2.3**: System shall validate required fields before saving  
**FR-2.4**: System shall display list of active customers  
**FR-2.5**: System shall provide customer search by name or phone  
**FR-2.6**: System shall allow soft-deleting customers (set is_active = false)  
**FR-2.7**: System shall display customer details with payment history  
**FR-2.8**: Default start date shall be current date

### 5.3 Payment Management

**FR-3.1**: System shall auto-generate monthly payment records on customer creation  
**FR-3.2**: Payment schedule shall include registration month (fix for customers registered after 5th)  
**FR-3.3**: Payment due date shall be 5th of each month  
**FR-3.4**: System shall allow marking payments as paid/unpaid  
**FR-3.5**: System shall record paid_date when payment marked paid  
**FR-3.6**: System shall allow reverting paid payments to unpaid  
**FR-3.7**: System shall calculate total paid and pending amounts per customer  
**FR-3.8**: System shall provide monthly payment filtering  
**FR-3.9**: "All Months + Pending" filter shall show all historical pending payments

### 5.4 Dashboard & Reporting

**FR-4.1**: Dashboard shall display total active customers count  
**FR-4.2**: Dashboard shall display current month paid/pending counts  
**FR-4.3**: Dashboard shall display current month total collection amount  
**FR-4.4**: Dashboard shall list today's pending follow-ups with days overdue  
**FR-4.5**: Dashboard shall provide quick navigation to all screens  
**FR-4.6**: Monthly Collections screen shall display month-wise collection summary  
**FR-4.7**: Collections shall show: month/year, total amount, payment count, customer count  
**FR-4.8**: Grand total of all collections shall be displayed

### 5.5 Reminder System

**FR-5.1**: System shall provide manual "Send Reminder" button on dashboard and customer details  
**FR-5.2**: System shall send WhatsApp messages via Twilio  
**FR-5.3**: Reminder messages shall be personalized with customer name, amount, due date, days overdue  
**FR-5.4**: System shall format phone numbers automatically (add +91 country code)  
**FR-5.5**: Reminder button shall show "✅ Sent Today" after sending  
**FR-5.6**: Reminder status shall persist for entire day (stored in localStorage)  
**FR-5.7**: System shall provide different message templates based on overdue status:
- 0 days: Friendly reminder
- 1-5 days: First reminder
- 6-10 days: Urgent reminder
- 11+ days: Final reminder

**FR-5.8**: System shall support automated daily reminders (scheduled at 9 AM)  
**FR-5.9**: System shall log all reminder attempts  
**FR-5.10**: System shall provide dry-run mode (ENABLE_WHATSAPP=false) for testing

### 5.6 User Interface

**FR-6.1**: UI shall be mobile-responsive (works on phones and tablets)  
**FR-6.2**: UI shall provide clear navigation between screens  
**FR-6.3**: System shall display loading indicators during API calls  
**FR-6.4**: System shall show success/error messages for user actions  
**FR-6.5**: Forms shall validate data before submission  
**FR-6.6**: Phone number field shall provide real-time uniqueness feedback (removed - now allows duplicates)  
**FR-6.7**: Branding shall display "Vaishnavi Silks Kanapuraka" on all screens  
**FR-6.8**: Footer shall display "Powered by CM"

---

## 6. Non-Functional Requirements

### 6.1 Performance
- **NFR-1.1**: Dashboard shall load in < 2 seconds
- **NFR-1.2**: Customer list shall paginate for > 100 customers
- **NFR-1.3**: Search results shall display within 500ms
- **NFR-1.4**: Payment marking shall respond immediately (< 500ms)

### 6.2 Usability
- **NFR-2.1**: System shall be usable by non-technical shop owners
- **NFR-2.2**: UI shall follow mobile-first design principles
- **NFR-2.3**: Touch targets shall be minimum 44x44 pixels
- **NFR-2.4**: Text shall be readable without zooming (minimum 14px font)

### 6.3 Reliability
- **NFR-3.1**: System uptime shall be 99% during business hours
- **NFR-3.2**: Data shall be persisted to disk immediately
- **NFR-3.3**: Failed reminder sends shall be logged for manual follow-up
- **NFR-3.4**: System shall handle database connection errors gracefully

### 6.4 Security
- **NFR-4.1**: Passwords shall never be stored in plain text
- **NFR-4.2**: API tokens shall expire after 24 hours
- **NFR-4.3**: Twilio credentials shall be stored in environment variables
- **NFR-4.4**: .env file shall not be committed to version control

### 6.5 Maintainability
- **NFR-5.1**: Code shall follow Python PEP 8 style guidelines
- **NFR-5.2**: API endpoints shall be documented via Swagger UI
- **NFR-5.3**: Database schema shall support future migrations
- **NFR-5.4**: Comprehensive documentation shall be provided

### 6.6 Scalability
- **NFR-6.1**: System shall support up to 500 customers
- **NFR-6.2**: Database shall handle 6000+ payment records
- **NFR-6.3**: Scheduler shall process 100+ reminders in < 5 minutes

---

## 7. High Level Architecture

### 7.1 Architecture Style
**Three-Tier Web Architecture**

```
┌─────────────────────────────────────────────────────┐
│                 Presentation Layer                   │
│  (HTML/CSS/JavaScript - Mobile Responsive)          │
│  - Login Screen                                      │
│  - Dashboard                                         │
│  - Customer Management                               │
│  - Payment Tracking                                  │
│  - Monthly Collections                               │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS/REST API
                   │ (JSON)
┌──────────────────▼──────────────────────────────────┐
│              Application Layer                       │
│           (FastAPI Backend)                          │
│  ┌─────────────────────────────────────────┐        │
│  │  API Controllers                         │        │
│  │  - Auth Router                           │        │
│  │  - Customer Router                       │        │
│  │  - Payment Router                        │        │
│  │  - Dashboard Router                      │        │
│  │  - Reminder Router                       │        │
│  └─────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────┐        │
│  │  Business Logic                          │        │
│  │  - CRUD Operations                       │        │
│  │  - Payment Schedule Generator            │        │
│  │  - Reminder Service                      │        │
│  │  - Authentication Handler                │        │
│  └─────────────────────────────────────────┘        │
└──────────────────┬──────────────────────────────────┘
                   │ SQLAlchemy ORM
┌──────────────────▼──────────────────────────────────┐
│               Data Layer                             │
│           (SQLite Database)                          │
│  - customers table                                   │
│  - payments table                                    │
│  - users table                                       │
└──────────────────────────────────────────────────────┘

External Integration:
┌──────────────────────────────────────────────────────┐
│            Twilio WhatsApp API                       │
│  - Send WhatsApp messages                            │
│  - Sandbox for testing                               │
│  - Production WhatsApp Business API                  │
└──────────────────────────────────────────────────────┘

Scheduler:
┌──────────────────────────────────────────────────────┐
│          APScheduler (Background)                    │
│  - Daily 9 AM reminder job                           │
│  - Checks pending payments                           │
│  - Sends automated reminders                         │
└──────────────────────────────────────────────────────┘
```

### 7.2 Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (SPA)                     │
├──────────────────────┬──────────────────────────────┤
│  app.js              │  API Client Functions         │
│  - Login/Logout      │  - apiCall()                  │
│  - Dashboard Logic   │  - State Management           │
│  - Customer CRUD     │  - localStorage (auth token)  │
│  - Payment Tracking  │  - Reminder tracking          │
│  - Collections View  │                               │
└──────────────────────┴──────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   Backend API                        │
├──────────────────────────────────────────────────────┤
│  main.py             - FastAPI app entry point       │
│  config.py           - Settings & environment vars   │
│  database.py         - DB session management         │
│  models.py           - SQLAlchemy models             │
│  schemas.py          - Pydantic validation schemas   │
│  crud.py             - Database operations           │
│  auth.py             - JWT authentication            │
│  reminders.py        - Reminder service & scheduler  │
│  twilio_service.py   - WhatsApp integration          │
├──────────────────────────────────────────────────────┤
│  API Routers:                                        │
│  - api/auth.py       - Login/Register endpoints      │
│  - api/customers.py  - Customer CRUD endpoints       │
│  - api/payments.py   - Payment management endpoints  │
│  - api/dashboard.py  - Dashboard stats & collections │
│  - api/reminders.py  - Manual reminder endpoints     │
└──────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              Utility Scripts                         │
├──────────────────────────────────────────────────────┤
│  create_demo_data.py      - Generate test data       │
│  view_database.py         - View DB contents         │
│  check_customer.py        - Check phone numbers      │
│  delete_customer.py       - Manage customer status   │
│  migrate_database.py      - Schema migrations        │
│  fix_payments.py          - Regenerate schedules     │
│  test_twilio.py           - Test WhatsApp setup      │
│  check_twilio.py          - Verify Twilio config     │
└──────────────────────────────────────────────────────┘
```

### 7.3 Deployment Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Client Devices                       │
│  - Shop Owner's Phone (Mobile Browser)               │
│  - Staff Laptop (Desktop Browser)                    │
│  - Tablet (Mobile Browser)                           │
└───────────────────┬──────────────────────────────────┘
                    │
                    │ HTTP/HTTPS
                    │
┌───────────────────▼──────────────────────────────────┐
│             Local Network / Internet                  │
│  IP: 192.168.0.103:8000 (LAN)                        │
│  OR: Public IP:8000 (if deployed)                    │
└───────────────────┬──────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────┐
│           Windows PC / Server (Host Machine)          │
│  ┌────────────────────────────────────────────┐      │
│  │  Python Virtual Environment (venv)         │      │
│  │  ┌──────────────────────────────────────┐  │      │
│  │  │  Uvicorn ASGI Server                 │  │      │
│  │  │  (Port 8000)                         │  │      │
│  │  │  - Auto-reload enabled               │  │      │
│  │  │  - Host: 0.0.0.0 (all interfaces)    │  │      │
│  │  └───────────┬──────────────────────────┘  │      │
│  │              │                              │      │
│  │  ┌───────────▼──────────────────────────┐  │      │
│  │  │  FastAPI Application                 │  │      │
│  │  │  - Routes all HTTP requests          │  │      │
│  │  │  - Serves static files               │  │      │
│  │  │  - API endpoints                     │  │      │
│  │  └───────────┬──────────────────────────┘  │      │
│  │              │                              │      │
│  │  ┌───────────▼──────────────────────────┐  │      │
│  │  │  SQLite Database                     │  │      │
│  │  │  File: payment_reminder.db           │  │      │
│  │  └──────────────────────────────────────┘  │      │
│  │                                              │      │
│  │  ┌──────────────────────────────────────┐  │      │
│  │  │  APScheduler (Background Thread)     │  │      │
│  │  │  - Runs daily reminder job @ 9 AM    │  │      │
│  │  └──────────────────────────────────────┘  │      │
│  └──────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────┘
                    │
                    │ HTTPS API
                    │
┌───────────────────▼──────────────────────────────────┐
│              Twilio WhatsApp API                      │
│  - Receives message requests                          │
│  - Formats and sends WhatsApp messages                │
│  - Returns delivery status                            │
└──────────────────────────────────────────────────────┘
```

---

## 8. Data Model

### 8.1 Entity Relationship Diagram

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ username (UNIQUE)   │
│ hashed_password     │
│ email               │
│ shop_name           │
│ is_active           │
│ created_at          │
│ updated_at          │
└─────────────────────┘

┌─────────────────────┐
│     customers       │
├─────────────────────┤                ┌─────────────────────┐
│ id (PK)             │                │     payments        │
│ name                │                ├─────────────────────┤
│ phone (INDEXED)     │◄───────────────│ id (PK)             │
│ monthly_amount      │     1      *   │ customer_id (FK)    │
│ start_date          │                │ amount              │
│ duration_months     │                │ due_date            │
│ total_paid          │                │ payment_month       │
│ total_pending       │                │ payment_year        │
│ is_active           │                │ is_paid             │
│ created_at          │                │ paid_date           │
│ updated_at          │                │ created_at          │
└─────────────────────┘                │ updated_at          │
                                       └─────────────────────┘
```

### 8.2 Table Definitions

**users** table:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    shop_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**customers** table:
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,  -- INDEXED but NOT UNIQUE (allows duplicates)
    monthly_amount FLOAT NOT NULL,
    start_date DATE NOT NULL,
    duration_months INTEGER NOT NULL,
    total_paid FLOAT DEFAULT 0,
    total_pending FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_is_active (is_active)
);
```

**payments** table:
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    due_date DATE NOT NULL,
    payment_month INTEGER NOT NULL,  -- 1-12
    payment_year INTEGER NOT NULL,   -- e.g., 2026
    is_paid BOOLEAN DEFAULT FALSE,
    paid_date DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_is_paid (is_paid),
    INDEX idx_due_date (due_date),
    INDEX idx_payment_month_year (payment_month, payment_year)
);
```

### 8.3 Data Rules & Constraints

1. **Customers**:
   - Phone numbers are indexed but not unique (allows family members with same number)
   - monthly_amount must be > 0
   - duration_months typically 6-12 months
   - total_paid and total_pending are calculated fields
   - Soft delete: is_active = false (data retained)

2. **Payments**:
   - Exactly duration_months payment records created per customer
   - due_date is always 5th of month
   - payment_month/payment_year indexed for fast filtering
   - paid_date only set when is_paid = true
   - Cannot delete payment records (only mark paid/unpaid)

3. **Users**:
   - username must be unique
   - Password never stored as plain text (bcrypt hashed)
   - Only one user per system currently (single-shop)

---

## 9. User Interface Design

### 9.1 Screen Flow

```
                    ┌──────────────┐
                    │ Login Screen │
                    └──────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
          ┌────────│   Dashboard   │────────┐
          │        └───────┬───────┘        │
          │                │                │
    ┌─────▼────┐    ┌─────▼──────┐   ┌────▼────────┐
    │Customers │    │  Payments  │   │ Collections │
    └─────┬────┘    └────────────┘   └─────────────┘
          │
          ▼
   ┌──────────────┐
   │Customer      │
   │Details       │
   └──────────────┘
          │
    ┌─────▼─────┐
    │   Add     │
    │ Customer  │
    └───────────┘
```

### 9.2 Key Design Principles

1. **Mobile-First**: All screens optimized for phone display
2. **Single Page App**: No full page reloads, smooth transitions
3. **Touch-Friendly**: Large buttons (minimum 44x44px)
4. **Clear Navigation**: Back buttons on all sub-screens
5. **Visual Feedback**: Loading spinners, success messages, disabled states
6. **Consistent Branding**: "Vaishnavi Silks Kanapuraka" on all screens

### 9.3 Color Scheme

- **Primary Green**: #4CAF50 (navigation, paid status)
- **Blue**: #2196F3 (links, secondary actions)
- **Red**: #f44336 (pending, delete actions)
- **Orange/Purple**: #6366f1 (reminder buttons)
- **Success Green**: #10b981 (collections, positive actions)
- **Background**: #f5f5f5 (light gray)
- **Cards**: #ffffff (white with shadow)

---

## 10. Integration Points

### 10.1 Twilio WhatsApp Integration

**Purpose**: Send payment reminder messages via WhatsApp

**Configuration**:
- Account SID: Unique Twilio account identifier
- Auth Token: API authentication token
- From Number: whatsapp:+14155238886 (sandbox) or business number
- Enable Flag: ENABLE_WHATSAPP (true/false)

**Message Flow**:
```
Frontend Click → API Endpoint → Reminder Service → 
Twilio Service → Format Message → Twilio API → 
WhatsApp → Customer Phone
```

**Sandbox Mode** (Testing):
- Customers must send "join [code]" to sandbox number
- Free for testing
- Limited to pre-registered numbers

**Production Mode** (Live):
- Requires WhatsApp Business API approval
- No joining required
- Costs ~₹0.40 per message in India

### 10.2 Future Integration Points

*Potential future integrations:*

1. **Accounting Software**: QuickBooks, Tally
2. **Payment Gateway**: Razorpay, Stripe (online payments)
3. **SMS Gateway**: MSG91, Twilio SMS (backup channel)
4. **Email**: SendGrid (email receipts)
5. **Analytics**: Google Analytics (usage tracking)

---

## Appendix

### Change History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Apr 2026 | Initial HLD and Requirements | System |

### Glossary

- **MSME**: Micro, Small, and Medium Enterprises
- **JWT**: JSON Web Token
- **ORM**: Object-Relational Mapping
- **CRUD**: Create, Read, Update, Delete
- **REST**: Representational State Transfer
- **API**: Application Programming Interface
- **UI**: User Interface
- **UX**: User Experience

### References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Document Status**: ✅ Approved and Implemented  
**Last Updated**: April 7, 2026
