# AI Phishing Detector 🛡️

A full-stack, machine-learning-powered web application that analyzes messages and emails to detect phishing attempts using Natural Language Processing (TF-IDF) and a Random Forest Classifier. 

The system features an Explainable AI interface that highlights the exact suspicious words that triggered the detection, and a continuous learning feedback loop that saves user corrections to the database for future retraining.

## 🚀 New Features & Updates
- **User Authentication**: Secure JWT-based Login and Registration. Each user has their own private scan history.
- **Admin Dashboard**: View system-wide analytics (total users, total scans, phishing detection rate) and securely trigger ML model retraining directly from the UI.
- **Scan History Page**: Users can browse through their previously scanned messages and view the AI's confidence score and prediction.
- **Enhanced Kenyan Dataset**: The Machine Learning model is now trained on **3,000+ records**, specifically enhanced with local Kenyan phishing tactics (e.g. M-Pesa suspension scams, Equity Bank KYC alerts, KRA penalty warnings, Helb/Hustler Fund scams).
- **SQLite Fallback**: Out-of-the-box local testing is now easier; the system falls back to a portable SQLite database if MySQL/MariaDB is not available.

## Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, React Router DOM
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Machine Learning:** Scikit-Learn (Random Forest, TF-IDF Vectorization)
- **Database:** SQLite (Fallback) / MariaDB / MySQL

---

## How to Run Locally

### 1. Prerequisites
- **Python 3.x** (with `pip`)
- **Node.js** (v18 or higher)

### 2. Clone the Repository
```bash
git clone https://github.com/frankireri/ai-phishing-detector.git
cd ai-phishing-detector
```

### 3. Backend Setup (Flask API & AI Model)
Open a terminal and navigate to the `backend` folder:
```bash
cd backend
```

Create a virtual environment and activate it:
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

**Train the AI Model:**
Before the API can run, you must train the Random Forest model on the dataset.
```bash
python train.py
```

**Start the Backend Server:**
```bash
python app.py
```
*(The Flask API will run on `http://localhost:5000`. It will automatically generate `phishing_db.sqlite` if no MySQL instance is detected, and populate it with a default `admin` user with password `admin`)*

### 4. Frontend Setup (React UI)
Open a **new** terminal window and navigate to the `frontend` folder:
```bash
cd frontend
```

Install the Node.js dependencies:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```

The frontend will start (usually on `http://localhost:5173`). Open that link in your browser to access the app! Log in with the `admin` account to access the Admin Dashboard.
