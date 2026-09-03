# PhishGuard AI - Backend (Flask)

This is the Flask + scikit-learn backend for the AI-based phishing detection system.

## Tech Stack
- **Flask 3** REST API
- **scikit-learn** for ML (Logistic Regression, Naïve Bayes, Random Forest, SVM)
- **NLTK** for NLP preprocessing
- **SQLAlchemy** with SQLite (default) or PostgreSQL
- **Flask-JWT-Extended** for auth
- **Flask-Limiter** for rate limiting
- **Joblib** for model serialization

## Local Setup

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

Copy `.env.example` to `.env` and edit if needed.

## Initialize Database & Train Model

```bash
python manage.py init-db
python manage.py create-admin
python manage.py train --dataset data/phishing_dataset.csv
```

The training step:
1. Loads and cleans the CSV (`text`, `label` columns)
2. Preprocesses text (tokenization, stopwords, lemmatization)
3. Extracts TF-IDF features
4. Trains 4 algorithms and compares them
5. Saves the best model to `models_storage/best_model.joblib`

## Run the API

```bash
python run.py
# or
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

The API will start on `http://localhost:5000`.

## API Endpoints

### Public
- `GET  /api/health` - Health check
- `GET  /api/info` - Service info
- `POST /api/predict` - Public prediction (rate-limited)
  ```json
  { "text": "Your message here", "type": "email" }
  ```
- `POST /api/predict/batch` - Batch predictions
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET  /api/training/metrics/latest` - View latest model metrics

### Authenticated (Bearer token)
- `GET  /api/auth/me` - Current user
- `POST /api/predict/logged` - Logged-in prediction (stored)
- `GET  /api/analytics/summary` - User stats
- `GET  /api/analytics/history` - Paginated history
- `GET  /api/analytics/dashboard` - Dashboard data
- `GET  /api/training/metrics` - All model metrics

### Admin only
- `POST /api/training/train` - Re-train all models
- `POST /api/training/activate/<id>` - Activate a model

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py        # Flask extensions
│   ├── errors.py            # Error handlers
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API blueprints
│   ├── services/            # ML + NLP services
│   └── utils/               # Helpers
├── data/                    # Training datasets
├── models_storage/          # Saved ML models
├── config.py
├── run.py                   # Entry point
├── manage.py                # CLI: init-db, create-admin, train
└── requirements.txt
```

## Environment Variables

| Var | Default | Description |
|-----|---------|-------------|
| `FLASK_ENV` | `development` | `development` or `production` |
| `SECRET_KEY` | dev key | Flask secret (CHANGE IN PROD) |
| `JWT_SECRET_KEY` | dev key | JWT secret (CHANGE IN PROD) |
| `DATABASE_URL` | sqlite:///phishing_detector.db | DB connection string |
| `ML_MODEL_PATH` | `models_storage` | Where to save/load model files |
| `ALLOWED_ORIGINS` | localhost:3000 | CORS allowed origins (comma-separated) |
| `RATE_LIMIT_PER_MINUTE` | `60` | Per-IP rate limit |
