# 💰 Payment Reminder Tool for MSME

**Vaishnavi Silks Kanapuraka - Payment Tracking System**

A simple, mobile-friendly web application that helps small shop owners (like saree shops, jewelry shops) manage monthly customer payment schemes and automate follow-ups via WhatsApp reminders.

---

## 📚 Documentation

- **[HLD & Requirements](HLD_AND_REQUIREMENTS.md)** - High level design, use cases, system architecture
- **[Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Build instructions, algorithms, API reference
- **[Render Deployment Guide](RENDER_DEPLOYMENT.md)** - Step-by-step guide to deploy on Render (free hosting)
- **[Original Requirements](ProjectRequirement.md)** - Initial project requirements

---

## 🌟 Features

- ✅ **Customer Management**: Add, view, search, and manage customer information
- 💳 **Payment Tracking**: Automatic monthly payment schedule generation
- 📊 **Dashboard**: Real-time statistics on payments and collections
- 📈 **Monthly Collections**: View month-wise collection analytics
- 🔔 **WhatsApp Reminders**: Automated reminders via Twilio WhatsApp API
- 📱 **Mobile-First Design**: Optimized for smartphones and tablets
- 🔐 **Secure Authentication**: JWT-based user authentication
- 🔄 **Payment Revert**: Ability to revert paid payments to unpaid
- 🗑️ **Customer Management**: Soft delete customers (data retained)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Windows/Linux/Mac
- 2GB RAM minimum

### Installation

1. **Create virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```powershell
   copy .env.example .env
   # Edit .env with your Twilio credentials (optional)
   ```

4. **Create demo data** (optional):
   ```powershell
   python create_demo_data.py
   ```

### Running the Application

**Start the server**:
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access the application**:
- **Local**: http://localhost:8000
- **Mobile (same network)**: http://YOUR_PC_IP:8000

**Demo Credentials**:
- Username: `demo`
- Password: `demo123`

---

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.109.0, Python 3.11+
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Authentication**: JWT (python-jose)
- **Scheduler**: APScheduler (background reminders)
- **Integration**: Twilio WhatsApp API

---

## 📱 WhatsApp Setup (Optional)

To enable WhatsApp reminders:

1. Sign up at [Twilio](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token
3. Join WhatsApp Sandbox (for testing)
4. Update `.env` file with credentials
5. Set `ENABLE_WHATSAPP=true`
6. Run: `python check_twilio.py` to verify

**Detailed Setup**: See [Technical Documentation](TECHNICAL_DOCUMENTATION.md#33-twilio-whatsapp-setup)

---

## 📁 Project Structure

```
ShopProject/
├── app/                      # Backend application
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Database models
│   ├── crud.py              # Business logic
│   ├── twilio_service.py    # WhatsApp integration
│   └── api/                 # API endpoints
├── static/                   # Frontend (HTML, CSS, JS)
├── payment_reminder.db      # SQLite database
├── requirements.txt         # Dependencies
└── Utility scripts (*.py)   # Helper tools
```

---

## 🧪 Testing

```powershell
# Test Twilio configuration
python check_twilio.py

# Interactive Twilio test
python test_twilio.py

# View database contents
python view_database.py

# Check customer by phone
python check_customer.py 9876543210
```

---

## 📖 API Documentation

**Automatic API Docs**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Complete API Reference**: See [Technical Documentation](TECHNICAL_DOCUMENTATION.md#6-api-reference)

---

## 🎯 Use Cases

1. **Add Customer** → Auto-generate 12 monthly payment records
2. **Mark Payment** → Update paid/pending status
3. **Send Reminder** → WhatsApp message to customer
4. **View Collections** → Month-wise collection analytics
5. **Dashboard** → Real-time statistics and pending follow-ups

**Detailed Use Cases**: See [HLD & Requirements](HLD_AND_REQUIREMENTS.md#3-use-cases)

---

## 🔧 Utility Scripts

| Script | Purpose |
|--------|---------|
| `create_demo_data.py` | Generate test data (5 customers + demo user) |
| `view_database.py` | View database contents |
| `check_customer.py` | Check customer by phone number |
| `delete_customer.py` | Soft delete or reactivate customer |
| `migrate_database.py` | Apply database schema changes |
| `fix_payments.py` | Regenerate payment schedules |
| `test_twilio.py` | Test WhatsApp integration |
| `check_twilio.py` | Verify Twilio configuration |

---

## 🚀 Deployment

### Local Network (Development)
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Access from any device on same WiFi: `http://192.168.x.x:8000`

### Production Options

#### 🌐 Render (Recommended - Free Tier Available)
**✅ Super easy deployment with GitHub integration**
- Free SSL/HTTPS included
- No credit card required
- Auto-deploy on Git push
- Free PostgreSQL database option

**📖 [Complete Render Deployment Guide →](RENDER_DEPLOYMENT.md)**

Quick steps:
1. Generate SECRET_KEY: `python generate_secret_key.py`
2. Push to GitHub
3. Connect to Render
4. Deploy! 🚀

#### Other Options
- **Railway**: Another great free option with GitHub deploy
- **Linux Server**: Ubuntu + NGINX (for full control)
- **DigitalOcean/AWS**: For larger scale deployments

**Full Deployment Guide**: See [Technical Documentation](TECHNICAL_DOCUMENTATION.md#8-deployment-guide)

---

## 🐛 Troubleshooting

### Common Issues

**Server won't start?**
- Activate virtual environment first: `venv\Scripts\Activate.ps1`
- Check all dependencies installed: `pip install -r requirements.txt`

**WhatsApp not sending?**
- Verify ENABLE_WHATSAPP=true in `.env`
- Ensure you joined WhatsApp sandbox
- Run: `python check_twilio.py`
- Restart server after .env changes

**Payment schedule missing months?**
- Run: `python fix_payments.py <phone_number>`

**More Issues**: See [Technical Documentation](TECHNICAL_DOCUMENTATION.md#10-troubleshooting)

---

## 📦 Features Overview

### Customer Management
- Add customer with name, phone, monthly amount, duration
- Duplicate phone numbers allowed (family members)
- Search by name or phone
- View customer payment history
- Soft delete (data retained)

### Payment Tracking
- Auto-generate monthly payments (includes registration month)
- Due date: 5th of each month
- Mark paid/unpaid
- Revert paid to unpaid
- Track total paid and pending per customer

### Dashboard
- Total active customers
- Current month statistics (paid/pending/collections)
- Today's pending follow-ups with days overdue
- Quick navigation buttons
- Real-time updates

### Reminders
- Manual "Send Reminder" button (dashboard & customer details)
- WhatsApp integration via Twilio
- Personalized messages with customer name, amount, due date
- Smart tracking: "Sent Today" persists for entire day
- Different message templates based on days overdue
- Optional: Automated daily reminders at 9 AM

### Analytics
- Monthly Collections screen
- Month-wise breakdown: amount, payment count, customer count
- Grand total of all collections
- Sortable by date (newest first)

### Mobile Experience
- Responsive design works on all screen sizes
- Touch-friendly buttons (44x44px minimum)
- Single Page App - no page reloads
- Fast loading and interactions
- Works in any modern browser

---

## 💡 Tips

- **Testing**: Use demo data to explore features
- **Backup**: Database is single file - easy to backup
- **WhatsApp**: Test with your own number first
- **Mobile**: Access from phone browser for best experience
- **Production**: Change SECRET_KEY in .env before deploying

---

## 📄 License

Proprietary - Vaishnavi Silks Kanapuraka

---

## 🙏 Support

For issues or questions:
- Check [Technical Documentation](TECHNICAL_DOCUMENTATION.md)
- Review [HLD & Requirements](HLD_AND_REQUIREMENTS.md)
- Verify Twilio setup: `python check_twilio.py`

---

**Built with ❤️ for MSME businesses**  
**Powered by CM | © 2026**

## 📖 Usage Guide

### First Time Setup

1. **Register a new account**:
   - Click on "Register" tab
   - Fill in username, email, password, and optional shop name
   - Click "Register"

2. **Login**:
   - Enter your username and password
   - Click "Login"

### Adding Customers

1. From the dashboard, click "➕ Add New Customer"
2. Fill in the customer details:
   - **Name**: Customer's full name
   - **Phone**: 10-digit phone number
   - **Monthly Amount**: Amount to be paid each month (e.g., ₹1000)
   - **Start Date**: When the scheme starts
   - **Duration**: Number of months (e.g., 12 months)
3. Click "Add Customer"

### Managing Payments

1. **View all customers**: Click "👥 View Customers"
2. **Click on a customer** to see their payment history
3. **Mark payments as paid**: Click "Mark Paid" button next to pending payments
4. **View all payments**: Click "💳 View Payments" from dashboard

### Dashboard Features

- **Statistics**: Total customers, paid/pending payments, collection amounts
- **Pending Follow-ups**: List of customers with overdue payments
- **Quick Actions**: Fast access to customer and payment management

## 🔧 Technical Details

### Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: JWT tokens with OAuth2

### Project Structure

```
ShopProject/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database setup
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   ├── crud.py          # Database operations
│   ├── reminders.py     # Reminder service
│   └── api/
│       ├── auth.py      # Auth endpoints
│       ├── customers.py # Customer endpoints
│       ├── payments.py  # Payment endpoints
│       └── dashboard.py # Dashboard endpoints
├── static/
│   ├── index.html       # Main HTML file
│   ├── styles.css       # Stylesheet
│   └── app.js           # JavaScript logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

### Database Schema

**Customers Table**:
- id, name, phone, monthly_amount, start_date, duration_months, is_active

**Payments Table**:
- id, customer_id, due_date, amount, is_paid, paid_date, payment_month, payment_year

**Users Table**:
- id, username, email, hashed_password, shop_name, is_active

## 🔔 Reminder System

The reminder system is designed to send automated reminders based on payment due dates:

- **Day 0**: Payment due today
- **Day 5**: First reminder (5 days overdue)
- **Day 10**: Second reminder (10 days overdue)
- **Day 15**: Final reminder (15 days overdue)
- **Week+**: Weekly reminders for significantly overdue payments

### Setting up Reminders

The reminder service is included but requires integration with a messaging service:

**For WhatsApp reminders**:
- Sign up for WhatsApp Business API (e.g., Twilio, MessageBird)
- Add API credentials to `.env` file
- Uncomment the actual sending code in `app/reminders.py`

**For SMS reminders**:
- Sign up for SMS service (e.g., Twilio, MSG91)
- Add API credentials to `.env` file
- Implement SMS sending in `app/reminders.py`

## 🔐 Security Considerations

- Change `SECRET_KEY` in `.env` for production
- Use HTTPS in production
- Set specific CORS origins in production
- Use a stronger database (PostgreSQL) for production
- Implement rate limiting for API endpoints

## 📱 Mobile Access

To access from mobile device:

1. Make sure your mobile and PC are on the same WiFi network
2. Find your PC's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)
3. On your mobile browser, visit: `http://YOUR_PC_IP:8000`

## 🚂 Deployment

### For Production Deployment:

1. **Use a production WSGI server**:
   ```powershell
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Deploy to cloud platforms**:
   - **Heroku**: Add `Procfile` with gunicorn command
   - **Railway**: Connect GitHub repo and deploy
   - **DigitalOcean**: Use App Platform or Droplet
   - **AWS**: Use Elastic Beanstalk or EC2

3. **Environment Variables**: Set all `.env` variables in your hosting platform

## 🐛 Troubleshooting

**"Module not found" error**:
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**"Address already in use" error**:
- Change port: `--port 8001`
- Or stop the process using port 8000

**Database errors**:
- Delete `payment_reminder.db` and restart the application
- Database will be recreated automatically

**Cannot access from mobile**:
- Check firewall settings
- Ensure both devices are on same network
- Try using PC's IP address instead of localhost

## 💡 Future Enhancements

- UPI payment link integration
- Native mobile app (Android/iOS)
- Multi-shop support
- Advanced analytics and reports
- Customer portal for self-service
- Automatic payment detection
- Export to Excel/PDF

## 📞 Support

For issues or questions, please check:
- The troubleshooting section above
- Console logs in browser (F12 → Console)
- Terminal logs where the server is running

## 📄 License

This project is created as a custom solution for MSME businesses. Feel free to modify and use as needed.

---

**Made with ❤️ for small business owners**
