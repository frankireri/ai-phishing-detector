# API Reference

Base URL: `https://your-api.example.com`

All endpoints return JSON. Errors follow the format:
```json
{ "error": "ErrorName", "message": "Description", "status": 400 }
```

## Authentication

Most protected endpoints expect an `Authorization: Bearer <token>` header. Obtain a token from `/api/auth/login` or `/api/auth/register`.

---

## `GET /api/health`

**Auth:** Public

```json
{
  "status": "healthy",
  "service": "AI Phishing Detector API",
  "version": "1.0.0",
  "model_loaded": true
}
```

## `GET /api/info`

**Auth:** Public

Returns service metadata and the loaded model info.

---

## `POST /api/predict`

**Auth:** Public (rate-limited)

Classify a single message.

**Request:**
```json
{
  "text": "URGENT: Your M-Pesa account has been suspended...",
  "type": "sms"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "prediction": "phishing",
    "confidence": 0.93,
    "model_used": "logistic_regression",
    "suspicious_keywords": ["urgent", "verify", "account"],
    "processing_time_ms": 12.4,
    "message_type": "sms",
    "input_length": 95
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | string | `"phishing"` or `"legitimate"` |
| `confidence` | float (0-1) | Probability of phishing |
| `model_used` | string | Algorithm name |
| `suspicious_keywords` | string[] | Matched keywords |
| `processing_time_ms` | float | Inference time |

## `POST /api/predict/batch`

**Auth:** Public (rate-limited)

Up to 100 messages at once.

```json
{
  "messages": [
    { "text": "...", "type": "email" },
    { "text": "...", "type": "sms" }
  ]
}
```

## `POST /api/predict/logged`

**Auth:** Required

Same as `/predict` but the result is stored in the database and tied to the user.

---

## `POST /api/auth/register`

**Auth:** Public

```json
{
  "email": "user@example.com",
  "username": "user",
  "password": "StrongP@ss123",
  "full_name": "Optional"
}
```

Returns JWT token and user object.

## `POST /api/auth/login`

**Auth:** Public

```json
{ "email": "user@example.com", "password": "StrongP@ss123" }
```

Either `email` or `username` works as the identifier.

## `GET /api/auth/me`

**Auth:** Required

Returns the authenticated user's profile.

---

## `GET /api/analytics/summary`

**Auth:** Required

Returns totals, phishing rate, average confidence, and a daily breakdown for the last 7 days.

## `GET /api/analytics/history?page=1&per_page=20`

**Auth:** Required

Paginated list of the user's predictions (admin sees all).

## `GET /api/analytics/dashboard`

**Auth:** Required

Aggregate stats + active model metrics for the dashboard.

---

## `GET /api/training/metrics`

**Auth:** Required

All recorded model metrics (most recent 50).

## `GET /api/training/metrics/latest`

**Auth:** Public

Latest metrics for all 4 algorithms + the currently loaded model.

## `POST /api/training/train`

**Auth:** Admin

Body:
```json
{ "dataset_path": "data/phishing_dataset.csv", "test_size": 0.2 }
```

Re-trains all models, persists metrics, and reloads the best one.

## `POST /api/training/activate/<metric_id>`

**Auth:** Admin

Marks a specific algorithm's metric record as the active model.
