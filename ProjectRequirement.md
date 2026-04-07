# 📄 Payment Reminder Tool for MSME (Saree Shop) – Requirements Document

## 1. 📌 Objective

Build a simple, mobile-friendly web application that helps small shop owners manage monthly customer payment schemes and automate follow-ups via reminders.

---

## 2. 🎯 Target Users

* Saree shop owners
* Jewelry shops running monthly schemes
* Small MSMEs with subscription-based customers

---

## 3. 🧵 Business Use Case

A shop owner has ~100 customers enrolled in a monthly payment scheme:

* Each customer pays ₹1000/month
* Duration: 12 months
* At the end, customer gets discount/benefit

### Current Problem:

* Manual tracking (notebook/Excel)
* Difficult to remember who paid
* Time-consuming follow-ups
* Missed payments → cash flow issues

---

## 4. ✅ Functional Requirements

### 4.1 Customer Management

* Add new customer with:

  * Name
  * Phone number
  * Monthly amount
  * Start date
  * Duration (months)
* View list of customers
* Edit/Delete customer (optional for MVP)

---

### 4.2 Payment Tracking

* Auto-generate monthly payment records for each customer
* Mark payment as:

  * Paid
  * Pending
* Store:

  * Payment date
  * Due month
* View payment history per customer

---

### 4.3 Dashboard

Display:

* Total customers
* Paid customers (current month)
* Pending customers
* Total collection (monthly)

---

### 4.4 Follow-up Management (Core Feature)

* Show “Today’s Pending Customers”
* Filter customers:

  * Paid / Unpaid
  * Month-wise

---

### 4.5 Reminder System

* Automatically send reminders:

  * 5th of every month
  * 10th (if unpaid)
  * 15th (final reminder)
* Manual “Send Reminder” option

---

### 4.6 Notification Channel

* WhatsApp messaging integration (preferred)
* SMS fallback (optional)

---

### 4.7 End-of-Year Summary

* Show:

  * Total paid by each customer
  * Pending dues
* Export/report (optional for MVP)

---

## 5. 📱 User Experience Requirements

* Mobile-first design
* Simple UI (usable by non-technical users)
* Max 2–3 clicks per action
* Large buttons, minimal text

### Core Screens:

1. Dashboard
2. Customer List
3. Payment Screen

---

## 6. ⚙️ Non-Functional Requirements

### Performance:

* Load within 2–3 seconds

### Scalability:

* Support up to 500 customers per shop (initially)

### Availability:

* Accessible via browser (no installation required)

### Security:

* Basic authentication (username/password)
* Secure customer data storage

---

## 7. 🧱 Technical Requirements

### Backend:

* Python (FastAPI)

### Database:

* SQLite (initial)
* Upgrade to PostgreSQL (later)

### Hosting:

* Cloud-based deployment

### Messaging Integration:

* WhatsApp API (via third-party provider)

---

## 8. 🔄 System Workflow

1. Shop owner adds customer
2. System generates monthly payment schedule
3. Each month:

   * Payments marked manually
   * System tracks pending dues
4. Reminder system triggers notifications
5. Dashboard reflects real-time status

---

## 9. 🚀 MVP Scope (Phase 1)

Include:

* Customer management
* Payment tracking
* Dashboard
* Basic reminder system (manual or simple automation)

Exclude (later phases):

* Payment gateway integration
* Advanced analytics
* Multi-user roles
* Mobile app

---

## 10. 📈 Future Enhancements

* UPI payment link integration
* Auto payment detection
* Customer login portal
* Multi-shop support
* Native mobile app

---

## 11. 💰 Business Model

* Subscription-based:

  * ₹299/month (up to 100 customers)
  * ₹499/month (higher tier)

---

## 12. 🎯 Success Criteria

* Reduces manual follow-up effort by >70%
* Improves on-time payments
* Easy adoption within 1 day by shop owner

---

## 13. 🧠 Key Design Principle

“Keep it simpler than a notebook”

---
