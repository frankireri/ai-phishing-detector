# PhishGuard AI 🛡️

> **AI-Based Phishing Detection System for Email and SMS Communication**
> Final Year Project · Catholic University of Eastern Africa (CUEA)
> **Student:** Maximillian Saitabau (1061592)
> **Supervisor:** Prof. Joel Barasa

A full-stack web application that uses **Machine Learning** and **Natural Language Processing** to detect phishing attempts in email and SMS messages. Built to address Kenya's growing cybersecurity threat from M-Pesa fraud, fake bank alerts, and government impersonation scams.

## ✨ Features

- 🤖 **4 ML models compared**: Logistic Regression, Naïve Bayes, Random Forest, SVM
- 🔤 **NLP pipeline**: tokenization, stop-word removal, lemmatization, TF-IDF
- ⚡ **Real-time classification** with confidence scores
- 🔍 **Suspicious keyword detection** for interpretability
- 📊 **Analytics dashboard** with charts (pie, bar, line)
- 🔐 **JWT authentication** with bcrypt password hashing
- 🚦 **Rate limiting** to prevent abuse
- 📱 **Responsive UI** built with Next.js + Tailwind CSS
- 🇰🇪 **Kenyan context**: trained on local phishing examples (M-Pesa, banks, KRA, KPLC)

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                Presentation Layer (Next.js)              │
│  Home · Login · Register · Dashboard · Analytics · About │
└────────────────────────┬─────────────────────────────────┘
                         │ REST / JSON
┌────────────────────────▼─────────────────────────────────┐
│          Application Layer (Flask + scikit-learn)        │
│  Auth · Prediction · Training · Analytics · Rate-limit   │
└────────────────────────┬─────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────▼─────────────────────────────────┐
│        Data Layer (PostgreSQL / SQLite + joblib)         │
│     Users · Predictions · Model Metrics · Model Files    │
└──────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Aiphishingdetector/
├── backend/                # Flask REST API
│   ├── app/
│   │   ├── routes/         # auth, predict, training, analytics, health
│   │   ├── services/       # preprocessing, trainer, model_loader
│   │   ├── models/         # SQLAlchemy models
│   │   └── utils/
│   ├── data/               # Training CSV
│   ├── models_storage/     # Saved joblib models
│   ├── config.py
│   ├── run.py
│   ├── manage.py           # CLI: init-db, create-admin, train
│   └── requirements.txt
├── frontend/               # Next.js (Vercel-ready)
│   ├── app/                # App Router
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   ├── package.json
│   └── vercel.json
├── docs/                   # Additional documentation
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- (Optional) PostgreSQL 13+ — SQLite works out of the box

### 1) Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt

# NLTK data
python -c "import nltk; [nltk.download(x, quiet=True) for x in ['stopwords','punkt','wordnet','punkt_tab']]"

cp .env.example .env
python manage.py init-db
python manage.py create-admin
python manage.py train --dataset data/phishing_dataset.csv
python run.py
```

Backend runs on `http://localhost:5000`.

### 2) Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:5000
npm run dev
```

Frontend runs on `http://localhost:3000`.

## 🌐 Deployment

### Frontend → Vercel
1. Push to GitHub
2. Import `frontend/` into Vercel
3. Set `NEXT_PUBLIC_API_URL` to your backend's public URL
4. Deploy

### Backend → Render / Railway / Fly.io / Heroku
The backend is a standard Flask app (gunicorn-ready via `run:app`).

**Render example (`render.yaml` / dashboard):**
- Build: `pip install -r requirements.txt`
- Start: `gunicorn -w 2 -b 0.0.0.0:$PORT run:app`
- Env vars: `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`, `ALLOWED_ORIGINS`

After deployment, set the frontend's `NEXT_PUBLIC_API_URL` to the backend's public URL, and add the Vercel domain to backend's `ALLOWED_ORIGINS`.

## 🧪 API Examples

### Health
```bash
curl http://localhost:5000/api/health
```

### Predict
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"URGENT: Your M-Pesa account has been suspended. Click http://mpesa-verify.duckdns.org","type":"sms"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cuea.ac.ke","password":"YourPassword123"}'
```

## 📊 Model Performance

The system trains and compares 4 algorithms on the dataset. Typical results on the bundled dataset (~150 samples) are modest; for production-quality results, train on a larger public corpus (e.g. UCI SMS Spam, Kaggle Phishing Email, Nazario phishing archive). Best model is auto-selected by F1-score and persisted to `models_storage/best_model.joblib`.

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion, Recharts |
| Backend | Flask 3, Flask-JWT-Extended, Flask-Limiter, SQLAlchemy |
| ML/NLP | scikit-learn, NLTK, TF-IDF, Joblib |
| Database | PostgreSQL / SQLite |
| Deployment | Vercel (frontend) · Render/Railway (backend) |

## 🔐 Security Features

- Password hashing with **bcrypt** (12 rounds)
- **JWT** authentication with 24h access tokens
- **Rate limiting** (60 req/min by default)
- **CORS** restricted to allowed origins
- **Input validation** on all endpoints
- **bcrypt**-based authentication
- Global error handlers (no stack-trace leaks in production)
- HTTPS recommended in production (handled by Vercel + your PaaS)

## 📚 Academic Context

This project was developed as a final year research project for the **Bachelor of Science in Computer Science** at the **Catholic University of Eastern Africa**. It demonstrates:

- Practical application of **supervised machine learning** to a real-world problem
- Use of **NLP techniques** (tokenization, stop-word removal, TF-IDF)
- Comparative analysis of **multiple algorithms** using standard metrics
- **Three-tier architecture** (Presentation, Application, Data)
- Modern **web development** with Next.js and Flask

## 📝 License

This project is for academic use only. © 2026 Maximillian Saitabau.

## 🤝 Acknowledgments

- Supervisor: Prof. Joel Barasa
- CUEA Faculty of Science
- Public datasets from Kaggle & UCI ML Repository
- Open source community
