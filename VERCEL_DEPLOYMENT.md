# 🚀 Vercel Deployment Guide - ReadEra

## Step 1: Push to GitHub

If not already done:
```bash
cd c:\Users\admin\Downloads\ReadEra
git init
git add .
git commit -m "ReadEra - Production Ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/readera.git
git push -u origin main
```

## Step 2: Create Vercel Account & Link Repository

1. Go to **https://vercel.com**
2. Sign up / Login with GitHub
3. Click "New Project"
4. Import the ReadEra repository
5. Select Python framework (or auto-detected)

## Step 3: Set Environment Variables

In Vercel Project Settings → Environment Variables, add:

```
GOOGLE_API_KEY = AIzaSyDIbBQPqj_dY5R5Y-kBjrEaUZYAvSCbVD4
ADMIN_EMAIL = admin@readera.com
ADMIN_PASSWORD = ReadEra@2024
```

## Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Get your live URL (e.g., `https://readera.vercel.app`)

## Step 5: Verify Deployment

After deployment, test:

```bash
# Homepage
curl https://readera.vercel.app/

# API endpoint
curl https://readera.vercel.app/api/books?limit=5

# Search
curl https://readera.vercel.app/api/books/search?q=yoga

# Admin verify
curl -X POST https://readera.vercel.app/api/admin/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@readera.com","password":"ReadEra@2024"}'
```

## Project Structure for Vercel

```
ReadEra/
├── api/
│   └── index.py              # Flask app (serverless function)
├── vercel.json              # Vercel configuration
├── .vercelignore            # Files to ignore
├── requirements.txt         # Python dependencies
├── index.html               # Homepage
├── browse.html              # Browse page
├── admin.html               # Admin panel
├── book.html                # Reading page
├── js/                       # JavaScript files
├── books_data/              # Book data JSON
├── *.html                   # Other pages
└── ...
```

## What's Configured

✅ Python 3.11+ with Flask 3.1.3  
✅ WSGI application for serverless  
✅ All API endpoints working  
✅ Static file serving  
✅ CORS enabled  
✅ Environment variables setup  

## Live Features

Once deployed:

- **Homepage**: https://your-domain.vercel.app/
- **Browse**: https://your-domain.vercel.app/browse.html
- **Admin**: https://your-domain.vercel.app/admin.html
- **API**: https://your-domain.vercel.app/api/books

## Troubleshooting

### Deploy fails with Python error
- Check requirements.txt has all dependencies
- Verify Python version in vercel.json

### 404 on static files
- Verify vercel.json routes are correct
- Check file paths are relative to project root

### API returns 500
- Check environment variables are set
- Verify books_data/index.json exists
- Check Vercel logs: `vercel logs` command

### Google Books API not working
- Ensure Books API is enabled in Google Cloud Console
- Check API key in Vercel environment variables

## Advanced Setup

### Custom Domain
1. In Vercel settings → Domains
2. Add your custom domain
3. Follow DNS setup instructions

### Auto-Deployment
- Enabled by default
- Push to `main` branch = auto deploy
- Create branch for staging

### Monitor Performance
- Vercel Dashboard → Analytics
- Check API response times
- Monitor serverless function usage

## Local Development

Test before deploying:
```bash
cd ReadEra
python -m pip install -r requirements.txt
python api/index.py
```

Then visit: http://localhost:5000

## Questions?

- Check Vercel docs: https://vercel.com/docs
- Flask on Vercel: https://vercel.com/docs/frameworks/flask
- Contact support: support@vercel.com

---

**ReadEra on Vercel** = Always-on, scalable, global CDN! 🌍
