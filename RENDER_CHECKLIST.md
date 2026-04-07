# 🚀 Quick Render Deployment Checklist

Follow these steps in order to deploy your app to Render:

## ✅ Pre-Deployment Checklist

- [ ] 1. **Generate SECRET_KEY**
  ```powershell
  python generate_secret_key.py
  ```
  Copy the generated key - you'll need it for Render!

- [ ] 2. **Test app locally one more time**
  ```powershell
  uvicorn app.main:app --reload
  ```
  Visit http://localhost:8000 and verify everything works

- [ ] 3. **Check .gitignore (already done!)**
  - ✅ `.env` is excluded
  - ✅ `*.db` is excluded
  - ✅ `venv/` is excluded

## 📤 Push to GitHub

- [ ] 4. **Initialize Git** (if not done)
  ```powershell
  git init
  git add .
  git commit -m "Initial commit - ready for Render"
  ```

- [ ] 5. **Create GitHub repository**
  - Go to https://github.com/new
  - Repository name: `vaishnavi-silks-payment-reminder`
  - Keep it Public or Private (both work with Render)
  - Don't initialize with README
  - Click "Create repository"

- [ ] 6. **Push to GitHub**
  ```powershell
  git remote add origin https://github.com/YOUR_USERNAME/vaishnavi-silks-payment-reminder.git
  git branch -M main
  git push -u origin main
  ```

## 🌐 Deploy on Render

- [ ] 7. **Sign up for Render**
  - Go to https://render.com
  - Click "Get Started for Free"
  - Sign up with GitHub (easiest option)

- [ ] 8. **Create Web Service**
  - Click "New +" → "Web Service"
  - Find and connect your repository
  - Click "Connect"

- [ ] 9. **Configure Service**
  Fill in these details:
  - **Name**: `vaishnavi-silks-payment-reminder`
  - **Region**: Choose closest (e.g., Oregon)
  - **Branch**: `main`
  - **Runtime**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - **Instance Type**: `Free`

- [ ] 10. **Add Environment Variables**
  Click "Advanced" → Add these:
  
  **Required:**
  ```
  SECRET_KEY = [paste the key from step 1]
  DATABASE_URL = sqlite:///./payment_reminder.db
  ```
  
  **Optional (for WhatsApp):**
  ```
  ENABLE_WHATSAPP = false
  TWILIO_ACCOUNT_SID = [your twilio SID]
  TWILIO_AUTH_TOKEN = [your twilio token]
  TWILIO_WHATSAPP_FROM = whatsapp:+14155238886
  ```

- [ ] 11. **Deploy!**
  - Click "Create Web Service"
  - Wait 2-5 minutes ⏳
  - Your app will be live! 🎉

## 🎯 Post-Deployment

- [ ] 12. **Test your live app**
  - Visit: `https://vaishnavi-silks-payment-reminder.onrender.com`
  - Click "Register" and create your account
  - Test all features

- [ ] 13. **Bookmark your app URL**

- [ ] 14. **Share with your team**

## ⚠️ Important Notes

**Free Tier Limitations:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds to wake up
- **SQLite data is LOST on restarts** 

**To Keep Data Forever:**
- Follow "Option 2" in [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- Add PostgreSQL database (also free!)
- Only takes 5 extra minutes

## 🐛 Troubleshooting

**App won't start?**
- Check "Logs" tab in Render dashboard
- Verify all environment variables are correct
- Make sure SECRET_KEY has no spaces

**Can't access app?**
- Wait 60 seconds after first deploy
- Try in incognito/private window
- Check deploy logs for errors

**Database keeps resetting?**
- This is normal with SQLite on free tier
- Upgrade to PostgreSQL (5 min setup, also free)
- See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) Option 2

## 🎉 Success!

Once deployed, your app URL is:
```
https://vaishnavi-silks-payment-reminder.onrender.com
```

Every time you push to GitHub, Render will auto-deploy! 🚀

---

**Need detailed help?** See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
