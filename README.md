# AI Phishing Detector 🛡️

A full-stack, machine-learning-powered web application that analyzes messages and emails to detect phishing attempts using Natural Language Processing (TF-IDF) and a Random Forest Classifier. 

The system features an Explainable AI interface that highlights the exact suspicious words that triggered the detection, and a continuous learning feedback loop that saves user corrections to a MariaDB database for future retraining.

## Tech Stack
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Machine Learning:** Scikit-Learn (Random Forest, TF-IDF Vectorization)
- **Database:** MariaDB / MySQL

---

## How to Run Locally on Another PC

To run this project on a new computer, follow these instructions step-by-step.

### 1. Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Python 3.x** (with `pip`)
- **Node.js** (v18 or higher)
- **MariaDB** or **MySQL** (e.g., via XAMPP, WAMP, or native installation)
- **Git**

### 2. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/frankireri/ai-phishing-detector.git
cd ai-phishing-detector
```

### 3. Database Setup
1. Start your MariaDB/MySQL server.
2. Create an empty database named `phishing_db`.
   *(If you are using XAMPP, open phpMyAdmin and create a new database called `phishing_db`)*.

> **Note:** The backend connects using the default credentials `root` with no password (`mysql+pymysql://root:@localhost/phishing_db`). If your database has a password, edit line 15 in `backend/app.py` to include it.

### 4. Backend Setup (Flask API & AI Model)
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
*(This will generate `model.pkl` and `vectorizer.pkl`)*

**Start the Backend Server:**
```bash
python app.py
```
The Flask API will now be running on `http://localhost:5000`.

### 5. Frontend Setup (React UI)
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

The frontend will start (usually on `http://localhost:5173`). Open that link in your browser, and the AI Phishing Detector is ready to use!
