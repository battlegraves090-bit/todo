# Render Deployment Guide

This guide will help you deploy your Django Todo App on Render's free tier.

## Prerequisites
- GitHub account with your repository pushed
- Render account (free at https://render.com)

## Deployment Steps

### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up with GitHub or email
3. Connect your GitHub account for easy deployment

### Step 2: Deploy Your Web Service

#### Via Render Dashboard (No Shell Required)

1. **Log in to Render Dashboard** at https://dashboard.render.com

2. **Click "New +"** and select **"Web Service"**

3. **Connect Repository**
   - Select "Deploy existing repository"
   - Choose `battlegraves090-bit/todo`
   - Click "Connect"

4. **Configure Web Service**
   Fill in the following:
   
   | Field | Value |
   |-------|-------|
   | **Name** | `todo-app` |
   | **Environment** | `Python 3` |
   | **Region** | `Oregon` (or closest to you) |
   | **Branch** | `main` |
   | **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
   | **Start Command** | `gunicorn todoapp.wsgi` |
   | **Plan** | `Free` |

5. **Add Environment Variables**
   Click "Add Environment Variable" and set:

   ```
   DEBUG = False
   ALLOWED_HOSTS = your-app-name.onrender.com
   SECRET_KEY = [generate a random secret key]
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

   **To generate a SECRET_KEY**, you can use:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Click "Create Web Service"**

### Step 3: Initial Deployment

1. Render will automatically start building your app
2. Monitor the build logs in the "Events" tab
3. Once deployment succeeds, you'll get a URL like: `https://todo-app.onrender.com`

### Step 4: Run Migrations (First Time Only)

Since you can't access the shell on the free tier, migrations run automatically via the Procfile:

```
release: python manage.py migrate
```

This runs before the web service starts.

### Step 5: Access Your App

- Visit your app URL: `https://todo-app.onrender.com`
- Create an account and start adding tasks!

## Database Note

**Important:** The free tier uses SQLite, which is stored on the Render container. 

⚠️ **Data will be lost when the container restarts** (Render restarts free tier apps periodically).

For production data persistence, upgrade to:
- **Render PostgreSQL** (free tier available, 90-day expiration)
- **External PostgreSQL database**

### To Use PostgreSQL (Optional):

1. In Render Dashboard, create a new **PostgreSQL** database
2. Copy the internal database URL
3. Add environment variable:
   ```
   DATABASE_URL = postgresql://user:password@host:port/dbname
   ```
4. Update `todoapp/settings.py` to use it (already configured with `dj-database-url`)
5. Re-deploy (migrations run automatically)

## Automatic Redeployments

To enable automatic redeployments when you push to GitHub:

1. In your Render service settings
2. Go to **"Deploy"** section
3. Enable **"Auto-Deploy"** for the `main` branch

## Common Issues

### "Static files not found"
- WhiteNoise is already configured in `middleware.py`
- Run: `python manage.py collectstatic --noinput`

### "Static site error"
- Check the build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies

### "Application Error"
- Click the service to view logs
- Common cause: Missing environment variables

### "Cannot access shell"
- Free tier doesn't include shell access
- Use automatic migrations or create a management command

## Monitoring & Management

### View Logs
1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. Real-time logs appear as your app runs

### Redeploy
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Or push to GitHub if auto-deploy is enabled

### Update Environment Variables
1. Go to service **"Environment"** tab
2. Edit variables
3. Changes take effect after redeploy

## Free Tier Limitations

- **Compute**: 0.5 CPU, 512 MB RAM
- **No public shell access**: Use scripts/management commands instead
- **Auto-suspend**: Apps go to sleep after 15 mins of inactivity
- **Cold start**: 50 seconds to wake up
- **Database**: SQLite (data loss on restart) or 90-day PostgreSQL trial

## Next Steps

1. ✅ Code pushed to GitHub
2. ✅ Deployment configured
3. Test the app at your Render URL
4. Consider upgrading for production use

## Support

- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Common issues: https://render.com/docs/troubleshooting
