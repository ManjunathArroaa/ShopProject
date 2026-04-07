# Technical Documentation

## Vaishnavi Silks Payment Reminder System

**Version:** 1.0  
**Technology Stack:** FastAPI + SQLite + Vanilla JavaScript + Twilio  
**Target Environment:** Windows Development, Production Linux

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack Details](#technology-stack-details)
3. [Build and Setup Instructions](#build-and-setup-instructions)
4. [Component Details](#component-details)
5. [Key Algorithms](#key-algorithms)
6. [API Reference](#api-reference)
7. [Database Schema](#database-schema)
8. [Deployment Guide](#deployment-guide)
9. [Testing Guide](#testing-guide)
10. [Troubleshooting](#troubleshooting)

---

## 1. System Architecture

### 1.1 Layered Architecture

```
┌──────────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Frontend)                 │
│  ┌────────────────────────────────────────────────┐  │
│  │  HTML5 + CSS3 (index.html, styles.css)        │  │
│  │  JavaScript SPA (app.js)                       │  │
│  │  - State Management (localStorage)             │  │
│  │  - API Client (Fetch API)                      │  │
│  │  - Screen Navigation                           │  │
│  │  - Form Validation                             │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
                         ↕ REST API (JSON)
┌──────────────────────────────────────────────────────┐
│          APPLICATION LAYER (Backend)                  │
│  ┌────────────────────────────────────────────────┐  │
│  │  FastAPI Application (main.py)                 │  │
│  │  - CORS Middleware                             │  │
│  │  - Static File Serving                         │  │
│  │  - Router Registration                         │  │
│  └────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────┐  │
│  │  API Routers (api/)                            │  │
│  │  - auth.py: Authentication endpoints           │  │
│  │  - customers.py: Customer CRUD                 │  │
│  │  - payments.py: Payment management             │  │
│  │  - dashboard.py: Statistics & collections      │  │
│  │  - reminders.py: Manual reminder trigger       │  │
│  └────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                          │  │
│  │  - crud.py: CRUD operations                    │  │
│  │  - auth.py: JWT & password handling            │  │
│  │  - reminders.py: Reminder service & scheduler  │  │
│  │  - twilio_service.py: WhatsApp integration     │  │
│  └────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────┐  │
│  │  Data Access Layer                             │  │
│  │  - models.py: SQLAlchemy models                │  │
│  │  - schemas.py: Pydantic validation             │  │
│  │  - database.py: Session management             │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
                         ↕ SQLAlchemy ORM
┌──────────────────────────────────────────────────────┐
│            DATA LAYER (Persistence)                   │
│  ┌────────────────────────────────────────────────┐  │
│  │  SQLite Database (payment_reminder.db)         │  │
│  │  - users table                                 │  │
│  │  - customers table                             │  │
│  │  - payments table                              │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘

        External Services
┌──────────────────────────────────────────────────────┐
│  Twilio WhatsApp API                                 │
│  - Message sending                                    │
│  - Delivery status                                    │
└──────────────────────────────────────────────────────┘

        Background Services
┌──────────────────────────────────────────────────────┐
│  APScheduler (Background Thread)                     │
│  - Daily reminder job (9 AM)                          │
│  - Check pending payments                             │
│  - Send automated reminders                           │
└──────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack Details

### 2.1 Backend Technologies

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.11+ | Core programming language |
| **FastAPI** | 0.109.0 | Modern web framework for building APIs |
| **Uvicorn** | 0.27.0 | ASGI server for FastAPI |
| **SQLAlchemy** | 2.0.25 | ORM for database operations |
| **Pydantic** | 2.5.3 | Data validation using Python type hints |
| **SQLite** | 3.x | Embedded relational database |
| **python-jose** | 3.3.0 | JWT token creation and verification |
| **passlib** | 1.7.4 | Password hashing with bcrypt |
| **bcrypt** | 4.0.1 | Secure password hashing algorithm |
| **APScheduler** | 3.10.4 | Task scheduling for automated reminders |
| **Twilio** | 8.10.0 | WhatsApp message sending |
| **python-dateutil** | 2.8.2 | Date manipulation utilities |
| **requests** | 2.31.0 | HTTP client library |
| **python-dotenv** | 1.0.0 | Environment variable loading |

### 2.2 Frontend Technologies

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure and semantic markup |
| **CSS3** | Styling, layout, responsiveness |
| **JavaScript (ES6+)** | Business logic, API calls, DOM manipulation |
| **Fetch API** | REST API communication |
| **localStorage** | Client-side data persistence (auth token, reminder tracking) |

### 2.3 Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **VS Code** | Code editor |
| **PowerShell** | Terminal/command execution |
| **Python venv** | Virtual environment isolation |

---

## 3. Build and Setup Instructions

### 3.1 Prerequisites

**System Requirements**:
- Windows 10/11 or Linux
- Python 3.11 or higher
- 2GB RAM minimum
- 500MB disk space

**Software Requirements**:
- Python 3.11+ installed
- Git (optional, for version control)
- Web browser (Chrome, Firefox, Safari, Edge)

### 3.2 Installation Steps

#### Step 1: Clone/Download Project

```powershell
# If using Git
git clone <repository-url>
cd ShopProject

# Or manually download and extract ZIP
```

#### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\Activate.ps1

# On Linux/Mac:
source venv/bin/activate
```

#### Step 3: Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Required Packages**:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
python-dotenv==1.0.0
pydantic-settings==2.1.0
python-multipart==0.0.6
passlib==1.7.4
bcrypt==4.0.1
python-jose[cryptography]==3.3.0
apscheduler==3.10.4
requests==2.31.0
python-dateutil==2.8.2
twilio==8.10.0
```

#### Step 4: Configure Environment

```powershell
# Copy example environment file
copy .env.example .env

# Edit .env file with your settings
notepad .env
```

**Required .env Configuration**:
```env
# Database
DATABASE_URL=sqlite:///./payment_reminder.db

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ENABLE_WHATSAPP=true

# Business
BUSINESS_NAME=Vaishnavi Silks Kanapuraka
```

#### Step 5: Initialize Database

```powershell
# Database is auto-created on first run
# To manually initialize:
python -c "from app.database import init_db; init_db()"
```

#### Step 6: Create Demo Data (Optional)

```powershell
# Generate test data: 5 customers + demo user
python create_demo_data.py

# Demo credentials: demo / demo123
```

#### Step 7: Run Application

```powershell
# Start development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Server will start at:
# http://localhost:8000  (local)
# http://192.168.0.103:8000  (LAN)
```

#### Step 8: Test Application

```powershell
# Open browser to:
http://localhost:8000

# Login with demo credentials:
# Username: demo
# Password: demo123
```

### 3.3 Twilio WhatsApp Setup

#### Step 1: Create Twilio Account

1. Visit: https://www.twilio.com/try-twilio
2. Sign up (free $15 credit)
3. Verify email and phone number

#### Step 2: Get Credentials

1. Login to: https://console.twilio.com
2. Copy **Account SID** (starts with "AC...")
3. Copy **Auth Token** (click to reveal)

#### Step 3: Join WhatsApp Sandbox

1. Go to: **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Note the sandbox number: **+1 415 523 8886**
3. Note the join code: e.g., "join happy-elephant"
4. From WhatsApp, send join code to sandbox number
5. Wait for confirmation message

#### Step 4: Update Configuration

```powershell
# Edit .env file
TWILIO_ACCOUNT_SID=ACc102b2f101d23a88a2615b76885179d5
TWILIO_AUTH_TOKEN=10f0dc01ee770bea827b9df4828011ef
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ENABLE_WHATSAPP=true
```

#### Step 5: Test Integration

```powershell
# Run test script
python test_twilio.py

# Or run diagnostic
python check_twilio.py

# Send test message from app Dashboard
```

### 3.4 Project Structure

```
ShopProject/
│
├── app/                          # Backend application
│   ├── __init__.py
│   ├── main.py                   # FastAPI entry point
│   ├── config.py                 # Settings & environment config
│   ├── database.py               # Database session management
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic validation schemas
│   ├── crud.py                   # CRUD operations
│   ├── auth.py                   # JWT authentication
│   ├── reminders.py              # Reminder service & scheduler
│   ├── twilio_service.py         # WhatsApp integration
│   └── api/                      # API route handlers
│       ├── __init__.py
│       ├── auth.py               # Login/register endpoints
│       ├── customers.py          # Customer CRUD endpoints
│       ├── payments.py           # Payment management endpoints
│       ├── dashboard.py          # Dashboard & collections endpoints
│       └── reminders.py          # Manual reminder endpoints
│
├── static/                       # Frontend assets
│   ├── index.html                # Single page application HTML
│   ├── styles.css                # CSS styles
│   └── app.js                    # Frontend JavaScript logic
│
├── venv/                         # Python virtual environment
│
├── .env                          # Environment variables (SECRET!)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
│
├── payment_reminder.db           # SQLite database file
│
├── ProjectRequirement.md         # Original requirements
├── README.md                     # Project overview
├── HLD_AND_REQUIREMENTS.md       # This file: High level design
├── TECHNICAL_DOCUMENTATION.md    # This file: Technical details
│
└── Utility Scripts:
    ├── create_demo_data.py       # Generate test data
    ├── view_database.py          # View database contents
    ├── check_customer.py         # Check phone numbers
    ├── delete_customer.py        # Manage customer status
    ├── migrate_database.py       # Database schema migrations
    ├── fix_payments.py           # Regenerate payment schedules
    ├── test_twilio.py            # Test WhatsApp integration
    └── check_twilio.py           # Verify Twilio configuration
```

---

## 4. Component Details

### 4.1 Backend Components

#### 4.1.1 main.py - Application Entry Point

**Purpose**: Initialize and configure FastAPI application

**Key Responsibilities**:
- Create FastAPI app instance
- Configure CORS middleware
- Register API routers
- Mount static file directory
- Define startup/shutdown events
- Serve main HTML page

**Code Structure**:
```python
app = FastAPI(title="Vaishnavi Silk - Payment Reminder System")

# Middleware
app.add_middleware(CORSMiddleware, ...)

# Routers
app.include_router(auth.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
# ... more routers

# Startup event
@app.on_event("startup")
async def startup_event():
    init_db()  # Initialize database
    # start_reminder_service()  # Optional: automated reminders

# Root endpoint
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
```

#### 4.1.2 models.py - Data Models

**Purpose**: Define database schema using SQLAlchemy ORM

**Models**:

**1. User Model**:
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100))
    shop_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**2. Customer Model**:
```python
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, index=True)  # NOT UNIQUE
    monthly_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    duration_months = Column(Integer, nullable=False)
    total_paid = Column(Float, default=0)
    total_pending = Column(Float, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    payments = relationship("Payment", back_populates="customer", cascade="all, delete-orphan")
```

**3. Payment Model**:
```python
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    payment_month = Column(Integer, nullable=False, index=True)  # 1-12
    payment_year = Column(Integer, nullable=False, index=True)
    is_paid = Column(Boolean, default=False, index=True)
    paid_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    customer = relationship("Customer", back_populates="payments")
```

#### 4.1.3 crud.py - CRUD Operations

**Purpose**: Database operations and business logic

**Key Functions**:

**1. Customer CRUD**:
```python
def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Create customer and generate payment schedule"""
    db_customer = Customer(...)
    db.add(db_customer)
    db.commit()
    generate_payment_schedule(db, db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    """Get all customers with pagination"""
    query = db.query(Customer)
    if active_only:
        query = query.filter(Customer.is_active == True)
    return query.offset(skip).limit(limit).all()

def delete_customer(db: Session, customer_id: int) -> bool:
    """Soft delete: set is_active = False"""
    customer = get_customer(db, customer_id)
    if customer:
        customer.is_active = False
        db.commit()
        return True
    return False
```

**2. Payment Generation Algorithm** (see section 5.1)

**3. Payment CRUD**:
```python
def mark_payment_paid(db: Session, payment_id: int) -> Optional[Payment]:
    """Mark payment as paid"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment:
        payment.is_paid = True
        payment.paid_date = datetime.utcnow()
        payment.updated_at = datetime.utcnow()
        db.commit()
        update_customer_totals(db, payment.customer_id)
        return payment
    return None
```

#### 4.1.4 auth.py - Authentication

**Purpose**: JWT token handling and password security

**Key Functions**:

**1. Password Hashing**:
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**2. JWT Token Creation**:
```python
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

**3. User Authentication**:
```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT token and return user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # ... validate and return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")
```

#### 4.1.5 reminders.py - Reminder Service

**Purpose**: Automated and manual reminder sending

**Key Components**:

**1. Reminder Service Class**:
```python
class ReminderService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start scheduler - runs daily at 9 AM"""
        self.scheduler.add_job(
            self.send_daily_reminders,
            'cron',
            hour=9,
            minute=0
        )
        self.scheduler.start()
    
    def send_daily_reminders(self):
        """Check pending payments and send reminders"""
        reminders = self.get_customers_to_remind(db)
        for reminder in reminders:
            message = self.create_reminder_message(reminder)
            self.send_reminder(reminder['phone'], message, ...)
```

**2. Reminder Categorization**:
```python
def get_customers_to_remind(self, db: Session):
    """Get customers needing reminders based on overdue days"""
    pending_payments = db.query(Payment).filter(
        Payment.is_paid == False,
        Payment.due_date <= today
    ).all()
    
    for payment in pending_payments:
        days_overdue = (today - payment.due_date).days
        
        # Categorize reminder level
        if days_overdue == 0:
            reminder_level = "due_today"
        elif days_overdue == 5:
            reminder_level = "first_reminder"
        elif days_overdue == 10:
            reminder_level = "second_reminder"
        # ...
```

#### 4.1.6 twilio_service.py - WhatsApp Integration

**Purpose**: Send WhatsApp messages via Twilio API

**Key Components**:

**1. Service Initialization**:
```python
class TwilioWhatsAppService:
    def __init__(self):
        self.enabled = settings.ENABLE_WHATSAPP
        self.client = None
        
        if self.enabled:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
```

**2. Phone Number Formatting**:
```python
def format_phone_number(self, phone: str) -> str:
    """Format phone to WhatsApp format"""
    # Remove spaces, dashes
    phone = phone.replace(" ", "").replace("-", "")
    
    # Add country code if missing (India +91)
    if not phone.startswith("+"):
        if not phone.startswith("91"):
            phone = "91" + phone
        phone = "+" + phone
    
    # Add whatsapp: prefix
    return f"whatsapp:{phone}"
```

**3. Message Sending**:
```python
def send_message(self, to_phone: str, message: str):
    """Send WhatsApp message"""
    try:
        to_number = self.format_phone_number(to_phone)
        
        twilio_message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_number
        )
        
        return {"success": True, "sid": twilio_message.sid}
    except Exception as e:
        return {"success": False, "message": str(e)}
```

### 4.2 Frontend Components

#### 4.2.1 app.js - Frontend Logic

**Purpose**: Single Page Application logic

**Key Functions**:

**1. Screen Management**:
```javascript
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show selected screen
    document.getElementById(screenId).classList.add('active');
    
    // Load data for screen
    if (screenId === 'dashboardScreen') loadDashboard();
    else if (screenId === 'customersScreen') loadCustomers();
    // ...
}
```

**2. API Communication**:
```javascript
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
    };
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: options.method || 'GET',
        headers,
        body: options.body ? JSON.stringify(options.body) : null
    });
    
    // Handle 204 No Content
    if (response.status === 204) return null;
    
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail);
    
    return data;
}
```

**3. Reminder Tracking** (localStorage):
```javascript
function wasReminderSentToday(customerId) {
    const todayKey = getTodayDateKey();  // "2026-04-07"
    const sentReminders = JSON.parse(localStorage.getItem('sentReminders') || '{}');
    return sentReminders[customerId] === todayKey;
}

function markReminderAsSent(customerId) {
    const todayKey = getTodayDateKey();
    const sentReminders = JSON.parse(localStorage.getItem('sentReminders') || '{}');
    sentReminders[customerId] = todayKey;
    localStorage.setItem('sentReminders', JSON.stringify(sentReminders));
}
```

**4. Dashboard Loading**:
```javascript
async function loadDashboard() {
    const stats = await apiCall('/api/dashboard/stats');
    const pending = await apiCall('/api/dashboard/pending-today');
    
    // Update statistics
    document.getElementById('totalCustomers').textContent = stats.total_customers;
    document.getElementById('paidThisMonth').textContent = stats.paid_this_month;
    // ...
    
    // Display pending customers with reminder buttons
    const pendingList = document.getElementById('pendingList');
    pendingList.innerHTML = pending.map(p => {
        const alreadySent = wasReminderSentToday(p.customer_id);
        return `
            <div class="pending-item">
                <div class="pending-info">
                    <h4>${p.customer_name}</h4>
                    <p>Amount: ${formatCurrency(p.amount)}</p>
                </div>
                <button onclick="sendReminder(${p.customer_id})" ${alreadySent ? 'disabled' : ''}>
                    ${alreadySent ? '✅ Sent Today' : '🔔 Reminder'}
                </button>
            </div>
        `;
    }).join('');
}
```

---

## 5. Key Algorithms

### 5.1 Payment Schedule Generation Algorithm

**Purpose**: Auto-generate monthly payment records for a customer

**Location**: `app/crud.py` → `generate_payment_schedule()`

**Algorithm**:

```python
def generate_payment_schedule(db: Session, customer: Customer):
    """
    Generate monthly payment records
    
    Rules:
    1. First payment ALWAYS uses registration month
    2. If registered after 5th: first due date = registration date
    3. If registered on/before 5th: first due date = 5th of that month
    4. Subsequent payments: 5th of each following month
    5. Generate exactly duration_months payments
    """
    
    start_date = customer.start_date
    current_date = start_date
    
    for i in range(customer.duration_months):
        if i == 0:
            # First payment - special handling
            if start_date.day > 5:
                # Registered after 5th: use registration date
                due_date = start_date
            else:
                # Registered on/before 5th: use 5th of registration month
                due_date = start_date.replace(day=5)
        else:
            # Subsequent payments: 5th of next month
            current_date = current_date + relativedelta(months=1)
            due_date = current_date.replace(day=5)
        
        payment = Payment(
            customer_id=customer.id,
            amount=customer.monthly_amount,
            due_date=due_date,
            payment_month=due_date.month,
            payment_year=due_date.year,
            is_paid=False
        )
        db.add(payment)
    
    db.commit()
```

**Example Scenarios**:

| Registration Date | Duration | First Payment Due | Subsequent Payments |
|------------------|----------|-------------------|---------------------|
| Apr 3, 2026 | 12 months | Apr 5, 2026 | May 5, Jun 5, ..., Mar 5 |
| Apr 6, 2026 | 12 months | Apr 6, 2026 | May 5, Jun 5, ..., Apr 5 |
| Apr 15, 2026 | 6 months | Apr 15, 2026 | May 5, Jun 5, ..., Sep 5 |

**Edge Cases Handled**:
- ✅ Registration on last day of month (e.g., Jan 31)
- ✅ February month handling (28/29 days)
- ✅ Month boundaries (Dec → Jan year rollover)

### 5.2 Reminder Categorization Algorithm

**Purpose**: Determine when to send reminders based on overdue days

**Location**: `app/reminders.py` → `get_customers_to_remind()`

**Algorithm**:

```python
def categorize_reminder(days_overdue: int) -> Optional[str]:
    """
    Categorize reminder level based on days overdue
    
    Returns:
        - "due_today": Payment due today (day 0)
        - "first_reminder": 5 days overdue
        - "second_reminder": 10 days overdue
        - "final_reminder": 15 days overdue
        - "overdue": > 15 days, every 7 days
        - None: No reminder needed
    """
    
    if days_overdue == 0:
        return "due_today"
    elif days_overdue == 5:
        return "first_reminder"
    elif days_overdue == 10:
        return "second_reminder"
    elif days_overdue == 15:
        return "final_reminder"
    elif days_overdue > 15 and days_overdue % 7 == 0:
        return "overdue"
    else:
        return None  # No reminder today
```

**Reminder Schedule Example**:

```
Day 0  (Apr 5):  🔔 Due today reminder
Day 1-4:         (Silent - no reminder)
Day 5  (Apr 10): 🔔 First reminder
Day 6-9:         (Silent)
Day 10 (Apr 15): 🔔 Second reminder
Day 11-14:       (Silent)
Day 15 (Apr 20): 🔔 Final reminder
Day 16-21:       (Silent)
Day 22 (Apr 27): 🔔 Weekly overdue reminder
Day 29 (May 4):  🔔 Weekly overdue reminder
Day 36 (May 11): 🔔 Weekly overdue reminder
... continues every 7 days
```

### 5.3 Phone Number Formatting Algorithm

**Purpose**: Convert Indian phone numbers to WhatsApp format

**Location**: `app/twilio_service.py` → `format_phone_number()`

**Algorithm**:

```python
def format_phone_number(phone: str) -> str:
    """
    Convert phone to WhatsApp format: whatsapp:+919876543210
    
    Input formats handled:
    - 9876543210
    - +919876543210
    - 919876543210
    - +91 98765 43210
    - 98765-43210
    
    Output: whatsapp:+919876543210
    """
    
    # Step 1: Remove formatting characters
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Step 2: Add country code if missing
    if not phone.startswith("+"):
        if not phone.startswith("91"):
            phone = "91" + phone  # Add India code
        phone = "+" + phone
    
    # Step 3: Add WhatsApp prefix
    if not phone.startswith("whatsapp:"):
        phone = f"whatsapp:{phone}"
    
    return phone
```

**Examples**:
```
Input                 → Output
9876543210            → whatsapp:+919876543210
+919876543210         → whatsapp:+919876543210
919876543210          → whatsapp:+919876543210
+91 98765 43210       → whatsapp:+919876543210
98765-43210           → whatsapp:+919876543210
```

### 5.4 Total Calculation Algorithm

**Purpose**: Calculate total paid and pending amounts for customer

**Location**: `app/crud.py` → `update_customer_totals()`

**Algorithm**:

```python
def update_customer_totals(db: Session, customer_id: int):
    """
    Recalculate total_paid and total_pending for customer
    
    Logic:
    - total_paid = SUM(amount WHERE is_paid = TRUE)
    - total_pending = SUM(amount WHERE is_paid = FALSE)
    """
    
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return
    
    # Calculate from payments
    payments = db.query(Payment).filter(Payment.customer_id == customer_id).all()
    
    total_paid = sum(p.amount for p in payments if p.is_paid)
    total_pending = sum(p.amount for p in payments if not p.is_paid)
    
    # Update customer record
    customer.total_paid = total_paid
    customer.total_pending = total_pending
    customer.updated_at = datetime.utcnow()
    
    db.commit()
```

**Called After**:
- Payment marked as paid
- Payment reverted to unpaid
- Customer scheme extended
- Payment amount modified

---

## 6. API Reference

### 6.1 Authentication Endpoints

#### POST /api/auth/login
**Purpose**: User login and JWT token generation

**Request**:
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=demo&password=demo123
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error** (401 Unauthorized):
```json
{
  "detail": "Incorrect username or password"
}
```

#### POST /api/auth/register
**Purpose**: Register new user

**Request**:
```http
POST /api/auth/register
Content-Type: application/json
Authorization: Bearer <token>

{
  "username": "shopowner",
  "password": "secure123",
  "email": "owner@shop.com",
  "shop_name": "Vaishnavi Silks"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "shopowner",
  "email": "owner@shop.com",
  "shop_name": "Vaishnavi Silks",
  "is_active": true,
  "created_at": "2026-04-07T10:30:00"
}
```

### 6.2 Customer Endpoints

#### POST /api/customers
**Purpose**: Create new customer

**Request**:
```http
POST /api/customers
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "monthly_amount": 2000,
  "start_date": "2026-04-07",
  "duration_months": 12
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "monthly_amount": 2000.0,
  "start_date": "2026-04-07",
  "duration_months": 12,
  "total_paid": 0.0,
  "total_pending": 24000.0,
  "is_active": true,
  "created_at": "2026-04-07T10:35:00",
  "updated_at": "2026-04-07T10:35:00"
}
```

Note: 12 payment records automatically generated.

#### GET /api/customers
**Purpose**: Get all customers

**Request**:
```http
GET /api/customers?skip=0&limit=100&active_only=true
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Rajesh Kumar",
    "phone": "9876543210",
    "monthly_amount": 2000.0,
    "start_date": "2026-04-07",
    "duration_months": 12,
    "total_paid": 4000.0,
    "total_pending": 20000.0,
    "is_active": true,
    "created_at": "2026-04-07T10:35:00",
    "updated_at": "2026-04-07T11:00:00"
  }
]
```

#### GET /api/customers/{id}
**Purpose**: Get customer details with payment history

**Request**:
```http
GET /api/customers/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "monthly_amount": 2000.0,
  "start_date": "2026-04-07",
  "duration_months": 12,
  "total_paid": 4000.0,
  "total_pending": 20000.0,
  "is_active": true,
  "payments": [
    {
      "id": 1,
      "amount": 2000.0,
      "due_date": "2026-04-07",
      "payment_month": 4,
      "payment_year": 2026,
      "is_paid": true,
      "paid_date": "2026-04-07T11:00:00"
    },
    {
      "id": 2,
      "amount": 2000.0,
      "due_date": "2026-05-05",
      "payment_month": 5,
      "payment_year": 2026,
      "is_paid": false,
      "paid_date": null
    }
  ]
}
```

#### DELETE /api/customers/{id}
**Purpose**: Soft delete customer

**Request**:
```http
DELETE /api/customers/1
Authorization: Bearer <token>
```

**Response** (204 No Content)

### 6.3 Payment Endpoints

#### GET /api/payments
**Purpose**: Get all payments with filtering

**Request**:
```http
GET /api/payments?month=4&year=2026&is_paid=false
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 2,
    "customer_id": 1,
    "customer_name": "Rajesh Kumar",
    "phone": "9876543210",
    "amount": 2000.0,
    "due_date": "2026-05-05",
    "payment_month": 5,
    "payment_year": 2026,
    "is_paid": false,
    "paid_date": null
  }
]
```

#### POST /api/payments/{id}/mark-paid
**Purpose**: Mark payment as paid

**Request**:
```http
POST /api/payments/2/mark-paid
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 2,
  "customer_id": 1,
  "amount": 2000.0,
  "is_paid": true,
  "paid_date": "2026-04-07T12:00:00"
}
```

#### PUT /api/payments/{id}
**Purpose**: Update payment (revert to unpaid)

**Request**:
```http
PUT /api/payments/2
Content-Type: application/json
Authorization: Bearer <token>

{
  "is_paid": false,
  "paid_date": null
}
```

**Response** (200 OK)

### 6.4 Dashboard Endpoints

#### GET /api/dashboard/stats
**Purpose**: Get dashboard statistics

**Request**:
```http
GET /api/dashboard/stats
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "total_customers": 6,
  "active_customers": 6,
  "paid_this_month": 3,
  "pending_this_month": 3,
  "total_collection_this_month": 6000.0,
  "pending_amount_this_month": 6000.0,
  "total_collection_overall": 18000.0
}
```

#### GET /api/dashboard/pending-today
**Purpose**: Get customers with pending payments for follow-up

**Request**:
```http
GET /api/dashboard/pending-today
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "customer_id": 1,
    "customer_name": "Rajesh Kumar",
    "phone": "9876543210",
    "amount": 2000.0,
    "due_date": "2026-04-05",
    "days_overdue": 2
  }
]
```

#### GET /api/dashboard/monthly-collections
**Purpose**: Get month-wise collection summary

**Request**:
```http
GET /api/dashboard/monthly-collections
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "collections": [
    {
      "month": "Apr",
      "year": 2026,
      "month_year": "Apr 2026",
      "total_amount": 6000.0,
      "payment_count": 3,
      "customer_count": 3
    },
    {
      "month": "Mar",
      "year": 2026,
      "month_year": "Mar 2026",
      "total_amount": 12000.0,
      "payment_count": 6,
      "customer_count": 5
    }
  ],
  "grand_total": 18000.0
}
```

### 6.5 Reminder Endpoints

#### POST /api/reminders/send/{customer_id}
**Purpose**: Send manual reminder to customer

**Request**:
```http
POST /api/reminders/send/1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Reminder sent to Rajesh Kumar"
}
```

**Error** (400 Bad Request):
```json
{
  "detail": "No pending payments found"
}
```

---

## 7. Database Schema

### 7.1 Complete Schema SQL

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    shop_name VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);

-- Customers Table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    monthly_amount FLOAT NOT NULL,
    start_date DATE NOT NULL,
    duration_months INTEGER NOT NULL,
    total_paid FLOAT DEFAULT 0,
    total_pending FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_is_active ON customers(is_active);

-- Payments Table
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    due_date DATE NOT NULL,
    payment_month INTEGER NOT NULL,
    payment_year INTEGER NOT NULL,
    is_paid BOOLEAN DEFAULT 0,
    paid_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE INDEX idx_payments_customer_id ON payments(customer_id);
CREATE INDEX idx_payments_is_paid ON payments(is_paid);
CREATE INDEX idx_payments_due_date ON payments(due_date);
CREATE INDEX idx_payments_month_year ON payments(payment_month, payment_year);
```

---

## 8. Deployment Guide

### 8.1 Local Deployment (Development)

**Already covered in Section 3**

### 8.2 Production Deployment Options

#### Option 1: Windows Server

**Requirements**:
- Windows Server 2019/2022
- Python 3.11+ installed
- IIS or NGINX (optional, for reverse proxy)
- SSL certificate (for HTTPS)

**Steps**:
1. Clone repository to server
2. Install Python dependencies
3. Configure .env with production settings
4. Change SECRET_KEY to strong random value
5. Set up Windows Service for auto-start
6. Configure firewall to allow port 8000
7. Set up reverse proxy (optional)
8. Configure SSL certificate

**Run as Windows Service**:
```powershell
# Use NSSM (Non-Sucking Service Manager) or Task Scheduler
# Or create Windows Service with pywin32
```

#### Option 2: Linux Server (VPS)

**Recommended Stack**: Ubuntu 22.04 + Gunicorn + NGINX

**Steps**:

1. **Install Dependencies**:
```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv nginx
```

2. **Clone and Setup**:
```bash
cd /var/www
git clone <repo-url> shopproject
cd shopproject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure Environment**:
```bash
cp .env.example .env
nano .env  # Edit with production values
```

4. **Create Systemd Service**:
```bash
sudo nano /etc/systemd/system/shopproject.service
```

```ini
[Unit]
Description=Shop Project FastAPI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/shopproject
Environment="PATH=/var/www/shopproject/venv/bin"
ExecStart=/var/www/shopproject/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

5. **Start Service**:
```bash
sudo systemctl enable shopproject
sudo systemctl start shopproject
sudo systemctl status shopproject
```

6. **Configure NGINX**:
```bash
sudo nano /etc/nginx/sites-available/shopproject
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/shopproject /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

7. **Setup SSL with Let's Encrypt**:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

#### Option 3: Cloud Platforms

**Railway.app** (Easiest):
1. Connect GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

**Heroku**:
1. Create `Procfile`: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. Add `runtime.txt`: `python-3.11.0`
3. Deploy via Git or GitHub integration

**DigitalOcean App Platform**:
1. Connect repository
2. Configure build/run commands
3. Set environment variables
4. Deploy

**AWS EC2**:
- Follow Linux deployment steps
- Use Amazon Linux 2 or Ubuntu AMI
- Configure security groups for ports 80/443

### 8.3 Production Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Set ENABLE_WHATSAPP to production credentials
- [ ] Use PostgreSQL instead of SQLite (for scalability)
- [ ] Enable HTTPS/SSL
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Set up firewall rules
- [ ] Use environment-specific .env files
- [ ] Enable automated reminders (uncomment in main.py)
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure CORS for specific origins only
- [ ] Set up rate limiting
- [ ] Enable database connection pooling

---

## 9. Testing Guide

### 9.1 Manual Testing

#### Test Case 1: User Registration and Login
```
1. Navigate to http://localhost:8000
2. Click "Register" tab
3. Enter: username=testuser, password=test123
4. Submit form
5. ✓ Success message appears
6. Switch to "Login" tab
7. Enter credentials
8. ✓ Redirect to Dashboard
```

#### Test Case 2: Add Customer
```
1. From Dashboard, click "➕ Add New Customer"
2. Enter:
   - Name: Test Customer
   - Phone: 9999999999
   - Amount: 1000
   - Duration: 12
3. Submit
4. ✓ Success message
5. ✓ Customer appears in list
6. Click customer
7. ✓ 12 payment records generated
```

#### Test Case 3: Mark Payment
```
1. View customer details
2. Find pending payment
3. Click "✓ Mark Paid"
4. ✓ Payment turns green
5. ✓ Total paid updates
6. ✓ Total pending decreases
```

#### Test Case 4: Send Reminder
```
1. Ensure WhatsApp sandbox joined
2. View customer with pending payment
3. Click "🔔 Send Reminder"
4. ✓ Button changes to "✅ Sent Today"
5. ✓ WhatsApp message received
6. ✓ Button stays disabled for rest of day
```

### 9.2 Automated Testing Scripts

#### test_api.py (API Testing)
```python
import requests

BASE_URL = "http://localhost:8000/api"

def test_login():
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "demo", "password": "demo123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

def test_get_customers(token):
    response = requests.get(
        f"{BASE_URL}/customers",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    customers = response.json()
    assert isinstance(customers, list)

# Run tests
if __name__ == "__main__":
    token = test_login()
    print("✓ Login test passed")
    test_get_customers(token)
    print("✓ Get customers test passed")
```

### 9.3 Utility Scripts Testing

**Test Database Utilities**:
```powershell
# View database contents
python view_database.py

# Check specific customer
python check_customer.py 9876543210

# Test Twilio configuration
python check_twilio.py

# Test Twilio messaging
python test_twilio.py
```

---

## 10. Troubleshooting

### 10.1 Common Issues

#### Issue 1: Server won't start
**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```powershell
# Activate virtual environment first
venv\Scripts\Activate.ps1

# Then start server
python -m uvicorn app.main:app --reload
```

#### Issue 2: WhatsApp messages not sending
**Error**: "Permission denied" from Twilio

**Causes & Solutions**:
1. **Customer hasn't joined sandbox**
   - Solution: Customer must send "join [code]" to sandbox number

2. **ENABLE_WHATSAPP is false**
   - Solution: Check .env file, set to true, restart server

3. **Invalid credentials**
   - Solution: Verify TWILIO_ACCOUNT_SID and AUTH_TOKEN in .env

4. **Server not restarted**
   - Solution: Restart server to load new.env changes

#### Issue 3: Database locked error
**Error**: `sqlite3.OperationalError: database is locked`

**Solution**:
```powershell
# SQLite can't handle concurrent writes
# Option 1: Stop other processes accessing DB
# Option 2: Switch to PostgreSQL for production

# Quick fix: restart server
```

#### Issue 4: Phone number already exists (old issue)
**Error**: `UNIQUE constraint failed: customers.phone`

**Solution**:
```powershell
# Run migration to remove unique constraint
python migrate_database.py
```

#### Issue 5: Payment schedule missing months
**Error**: Customer registered Apr 6, but April payment missing

**Solution**:
```powershell
# Regenerate payment schedule
python fix_payments.py <phone_number>

# Example:
python fix_payments.py 9876543210
```

### 10.2 Debug Mode

**Enable Debug Logging**:
```python
# In app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check Server Logs**:
- Watch terminal output when server running
- Look for ERROR or WARNING messages
- Check Twilio response codes

**Database Inspection**:
```powershell
# View all tables and data
python view_database.py

# Or use SQLite browser
sqlite3 payment_reminder.db
.tables
SELECT * FROM customers;
SELECT * FROM payments WHERE is_paid = 0;
```

### 10.3 Performance Issues

**If dashboard slow**:
```sql
-- Add indexes (already done in schema)
CREATE INDEX idx_payments_customer_id ON payments(customer_id);
CREATE INDEX idx_payments_is_paid ON payments(is_paid);

-- Or upgrade to PostgreSQL
```

**If API slow**:
- Enable database connection pooling
- Add caching (Redis)
- Optimize queries with .join()
- Paginate large result sets

---

## Appendix A: Configuration Reference

### Environment Variables (.env)

```env
# Database Configuration
DATABASE_URL=sqlite:///./payment_reminder.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# Security Settings
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_32_char_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ENABLE_WHATSAPP=true

# Business Configuration
BUSINESS_NAME=Vaishnavi Silks Kanapuraka
```

---

## Appendix B: Command Reference

### Development Commands

```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Access application
http://localhost:8000  # Local
http://192.168.0.103:8000  # LAN

# API documentation
http://localhost:8000/docs  # Swagger UI
http://localhost:8000/redoc  # ReDoc
```

### Database Commands

```powershell
# Create demo data
python create_demo_data.py

# View database contents
python view_database.py

# Migrate database schema
python migrate_database.py

# Fix payment schedules
python fix_payments.py <phone_number>

# Check customer details
python check_customer.py <phone_number>

# Manage customer status
python delete_customer.py soft_delete <phone_number>
python delete_customer.py reactivate <phone_number>
```

### Twilio Commands

```powershell
# Test Twilio configuration
python check_twilio.py

# Interactive Twilio test
python test_twilio.py
```

---

## Appendix C: Technology Justification

### Why FastAPI?
- ✅ Modern Python web framework
- ✅ Automatic API documentation (Swagger)
- ✅ Fast performance (async support)
- ✅ Type hints and data validation
- ✅ Easy to learn and use

### Why SQLite?
- ✅ Zero configuration
- ✅ Serverless (embedded database)
- ✅ Perfect for small-scale applications
- ✅ Easy backup (single file)
- ⚠️ Upgrade to PostgreSQL for > 500 customers

### Why Vanilla JavaScript?
- ✅ No build tools required
- ✅ Fast development for simple UI
- ✅ No framework learning curve
- ✅ Lightweight (< 50 KB total)
- ⚠️ Consider React/Vue for complex features

### Why Twilio?
- ✅ Reliable WhatsApp API
- ✅ Good documentation
- ✅ Free trial credit
- ✅ 98% message delivery rate
- ✅ Affordable pricing (~₹0.40/message in India)

---

**Document Status**: ✅ Complete and Verified  
**Last Updated**: April 7, 2026  
**Maintained By**: Development Team
