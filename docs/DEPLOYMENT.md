# PhishGuard AI - Deployment Guide

This document explains how to deploy the system to production.

## Architecture in Production

```
┌─────────────────┐    HTTPS    ┌──────────────────┐
│   Vercel CDN    │ ──────────► │  Flask Backend   │
│  (Next.js app)  │             │  (Render/Railway)│
└─────────────────┘             └────────┬──────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  PostgreSQL DB   │
                                │  (managed)       │
                                └──────────────────┘
```

## Step 1: Deploy Backend

### Option A: Render.com (recommended for free tier)

1. Push the repository to GitHub.
2. Sign in to [Render](https://render.com).
3. Click **New +** → **Web Service** → connect the repo.
4. Set the **Root Directory** to `backend`.
5. Configure:
   - **Environment**: `Python 3`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python -c "import nltk; [nltk.download(x, quiet=True) for x in ['stopwords','punkt','wordnet','punkt_tab']]" && python manage.py init-db && python manage.py train --dataset data/phishing_dataset.csv
     ```
   - **Start Command**: `gunicorn -w 2 -b 0.0.0.0:$PORT run:app`
   - **Plan**: Free
6. Add environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<random 64-char string>`
   - `JWT_SECRET_KEY=<random 64-char string>`
   - `DATABASE_URL=<postgres url from your managed DB>`
   - `ALLOWED_ORIGINS=https://your-app.vercel.app`
7. Click **Create Web Service** and wait for deploy.
8. Note the URL, e.g. `https://phishguard-api.onrender.com`.

### Option B: Railway.app

1. New Project → Deploy from GitHub repo.
2. Set **Root Directory** to `backend`.
3. Add the same env vars and start command as Render.
4. Railway auto-detects Python and runs `Procfile`.

### Option C: Docker (any VPS)

```bash
cd backend
docker build -t phishguard-api .
docker run -p 5000:5000 \
  -e SECRET_KEY=... \
  -e JWT_SECRET_KEY=... \
  -e DATABASE_URL=... \
  -e ALLOWED_ORIGINS=https://your-app.vercel.app \
  phishguard-api
```

## Step 2: Deploy Frontend to Vercel

1. Sign in to [Vercel](https://vercel.com).
2. **Add New Project** → Import your GitHub repo.
3. Set **Root Directory** to `frontend`.
4. Framework preset: **Next.js** (auto-detected).
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://phishguard-api.onrender.com` (your backend URL, NO trailing slash)
6. Click **Deploy**.

The Vercel deployment will provide a URL like `https://phishguard.vercel.app`.

## Step 3: Update Backend CORS

Go back to your backend host (Render / Railway) and update:
- `ALLOWED_ORIGINS` to include your Vercel URL.

Restart the backend. The frontend should now work end-to-end.

## Step 4: (Optional) Custom Domain

Both Vercel and Render support custom domains. Add a `CNAME` from `phishguard.yourdomain.com` → Vercel, and `api.yourdomain.com` → Render.

Then update env vars accordingly.

## Step 5: Train on Real Data (Recommended)

The bundled dataset has ~150 samples for demo purposes. For production-quality results, train on a larger public dataset:

- [Kaggle Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)
- [UCI SMS Spam Collection](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)
- [Nazario Phishing Corpus](https://monkey.org/~jose/phishing/)

Place your CSV in `backend/data/phishing_dataset.csv` (with `text` and `label` columns) and run:

```bash
python manage.py train --dataset data/phishing_dataset.csv
```

Then commit `models_storage/best_model.joblib` and `models_storage/tfidf_vectorizer.joblib` to your repo, or upload them to your backend host manually (or use a storage service like S3 / Cloudflare R2).

## Local Production-like Test

```bash
cd backend
FLASK_ENV=production gunicorn -w 2 -b 0.0.0.0:5000 run:app
```

```bash
cd frontend
NEXT_PUBLIC_API_URL=http://localhost:5000 npm run build && npm start
```

## Health Check

```bash
curl https://phishguard-api.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "AI Phishing Detector API",
  "version": "1.0.0",
  "model_loaded": true
}
```

## Troubleshooting

- **Model not loaded on backend startup**: Make sure `models_storage/best_model.joblib` exists. The startup hook will train one from `data/phishing_dataset.csv` if missing.
- **CORS errors**: Add the Vercel URL to `ALLOWED_ORIGINS` (comma-separated).
- **First request slow on Render free tier**: Cold start can take 30-50s. Upgrade plan or add a ping service.
- **NLTK LookupError**: Run the NLTK download command from the build step.
