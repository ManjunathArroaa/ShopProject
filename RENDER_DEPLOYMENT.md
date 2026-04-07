# Deploying to Render - Step by Step Guide

## ⚠️ Important Note About Free Tier
Render's **free tier uses ephemeral storage**, meaning:
- Your SQLite database will be **deleted every time the service restarts** (happens when inactive for 15+ minutes)
- To persist data, you'll need to upgrade to a paid plan OR use Render's PostgreSQL database (also has free tier)

For production use, I recommend using Render PostgreSQL (instructions included below).

---

## Option 1: Quick Deploy with SQLite (Data Will Not Persist)

### Step 1: Push Code to GitHub

1. **Initialize Git repository** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it: `vaishnavi-silks-payment-reminder`
   - Don't initialize with README (we already have files)
   - Click "Create repository"

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/vaishnavi-silks-payment-reminder.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Sign up on Render**:
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended for easy integration)

2. **Create New Web Service**:
   - Dashboard → Click "New +" → "Web Service"
   - Connect your GitHub repository: `vaishnavi-silks-payment-reminder`
   - Click "Connect"

3. **Configure the Service**:
   - **Name**: `vaishnavi-silks-payment-reminder`
   - **Region**: Choose closest to you (e.g., Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Select **Free**

4. **Add Environment Variables**:
   Click "Advanced" → Add Environment Variables:
   
   ```
   SECRET_KEY = your-secret-key-here-minimum-32-characters
   DATABASE_URL = sqlite:///./payment_reminder.db
   ENABLE_WHATSAPP = false
   ```

   Optional (if using Twilio):
   ```
   TWILIO_ACCOUNT_SID = your_twilio_account_sid
   TWILIO_AUTH_TOKEN = your_twilio_auth_token
   TWILIO_WHATSAPP_FROM = whatsapp:+14155238886
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://vaishnavi-silks-payment-reminder.onrender.com`

### Step 3: Create Demo User

After deployment, create a user account:
- Visit your app URL
- Click "Register"
- Create your admin account

---

## Option 2: Deploy with PostgreSQL (Data WILL Persist) ⭐ RECOMMENDED

### Step 1: Create PostgreSQL Database on Render

1. **Create Database**:
   - Render Dashboard → Click "New +" → "PostgreSQL"
   - **Name**: `vaishnavi-silks-db`
   - **Database**: `vaishnavi_silks`
   - **User**: `vaishnavi_admin` (auto-generated)
   - **Region**: Same as your web service
   - **Plan**: **Free**
   - Click "Create Database"

2. **Copy Connection Info**:
   - After creation, go to database page
   - Copy the **Internal Database URL** (starts with `postgresql://`)
   - Example: `postgresql://user:password@hostname/database`

### Step 2: Update Application for PostgreSQL

1. **Add PostgreSQL driver to requirements.txt**:
```bash
echo psycopg2-binary==2.9.9 >> requirements.txt
```

2. **Commit and push**:
```bash
git add requirements.txt
git commit -m "Add PostgreSQL support"
git push
```

### Step 3: Deploy Web Service with PostgreSQL

Follow **Option 1 Steps 1-2**, but in Step 2.4, use these environment variables:

```
SECRET_KEY = your-secret-key-here-minimum-32-characters
DATABASE_URL = [PASTE YOUR POSTGRESQL INTERNAL URL HERE]
ENABLE_WHATSAPP = false
```

The app will automatically use PostgreSQL instead of SQLite!

---

## Post-Deployment Setup

### 1. Test Your Application
Visit: `https://your-app-name.onrender.com`

### 2. Enable HTTPS (Already Done!)
Render provides free SSL certificates automatically. Your app is secure! 🔒

### 3. Custom Domain (Optional)
- Go to your web service settings
- Click "Custom Domain"
- Follow instructions to connect your domain

### 4. Enable WhatsApp Reminders (Optional)
1. Set environment variables:
   - `ENABLE_WHATSAPP=true`
   - Add Twilio credentials
2. Restart the service

---

## Important Notes

### Free Tier Limitations:
- ⏸️ **Service spins down after 15 minutes of inactivity**
- 🚀 **First request after inactivity takes ~30-60 seconds** (cold start)
- 💾 **SQLite data is lost on restart** (use PostgreSQL to persist data)
- 🔄 **750 hours/month free** (enough for one service running 24/7)

### Monitoring Your App:
- View logs: Service page → "Logs" tab
- Monitor metrics: Service page → "Metrics" tab
- Get notifications: Settings → "Notifications"

### Updating Your App:
Just push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```
Render will automatically redeploy! 🎉

---

## Troubleshooting

### App Not Starting?
1. Check logs in Render dashboard
2. Verify environment variables are set correctly
3. Make sure `requirements.txt` is up to date

### Database Connection Failed?
- Verify `DATABASE_URL` is correct
- For PostgreSQL: Use **Internal Database URL**, not External

### Static Files Not Loading?
- Static files are served from `/static/` path
- Render may need a few minutes to serve them properly after first deploy

### App Sleeping (Render Free Tier)?
- First request after 15 min inactivity will be slow (~30-60 sec)
- Consider using a free uptime monitor (e.g., UptimeRobot) to ping your app every 5 minutes
- Or upgrade to paid plan ($7/month) for always-on service

---

## Security Checklist

✅ `.env` file is in `.gitignore` (don't commit secrets!)  
✅ Use strong `SECRET_KEY` (32+ characters)  
✅ Set environment variables in Render dashboard, not in code  
✅ Use HTTPS (automatic with Render)  
✅ Change default demo password after deployment  

---

## Cost Summary

**Free Tier (What You Get):**
- ✅ Web service (750 hours/month)
- ✅ PostgreSQL database (90 days, then expires)
- ✅ Free SSL certificate
- ✅ Custom domain support
- ✅ Automatic deploys from GitHub

**Paid Plans (Optional):**
- Web Service: $7/month (no sleeping, more resources)
- PostgreSQL: $7/month (persistent, never expires)

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render account
3. ✅ Deploy web service
4. ✅ (Optional but recommended) Create PostgreSQL database
5. ✅ Register your admin account
6. ✅ Test all features
7. 🎉 Share your app!

Your app will be live at:  
**`https://your-app-name.onrender.com`**

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Congratulations! Your payment reminder tool will be live on the internet! 🚀**
