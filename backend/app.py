from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)
# Enable CORS so the React frontend can communicate with this API
CORS(app)

# Configure MariaDB connection
# Change username/password/database name if your local setup differs
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/phishing_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Database Model for Scan History
class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    suspicious_words = db.Column(db.Text, nullable=True) # Stored as JSON string
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure tables are created before first request
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Warning: Could not connect to MariaDB or create tables. Ensure MariaDB is running and the database 'phishing_db' exists.")
        print(f"Error: {e}")

# Load the trained model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
else:
    print("Warning: Model files not found. Please run train.py first.")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model not trained yet. Run train.py first.'}), 500
        
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided.'}), 400
        
    text = data['text']
    
    # Preprocess and extract features
    features = vectorizer.transform([text])
    
    # Predict
    prediction = model.predict(features)[0]
    
    # Get confidence score (probability of the predicted class)
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities) * 100
    
    # Extract suspicious words if phishing
    suspicious_words = []
    if prediction == 'phishing':
        feature_names = vectorizer.get_feature_names_out()
        coefficients = model.coef_[0]
        
        # Get the indices of the words present in the message
        feature_indices = features.nonzero()[1]
        
        # Create a list of (word, weight) for the present words
        word_weights = [(feature_names[idx], coefficients[idx]) for idx in feature_indices]
        
        # Sort by weight descending (highest positive weights are most "phishy")
        word_weights.sort(key=lambda x: x[1], reverse=True)
        
        # Get the top 5 words that contributed to phishing
        suspicious_words = [word for word, weight in word_weights if weight > 0][:5]
    
    # Save to MariaDB
    try:
        new_scan = ScanHistory(
            message_text=text,
            prediction=prediction,
            confidence=round(confidence, 2),
            suspicious_words=json.dumps(suspicious_words) if suspicious_words else None
        )
        db.session.add(new_scan)
        db.session.commit()
    except Exception as e:
        print(f"Failed to save to database: {e}")
        db.session.rollback()

    return jsonify({
        'prediction': prediction,
        'confidence': round(confidence, 2),
        'suspicious_words': suspicious_words
    })

@app.route('/history', methods=['GET'])
def get_history():
    try:
        # Fetch the 10 most recent scans
        scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(10).all()
        history = []
        for scan in scans:
            history.append({
                'id': scan.id,
                'message_text': scan.message_text,
                'prediction': scan.prediction,
                'confidence': scan.confidence,
                'suspicious_words': json.loads(scan.suspicious_words) if scan.suspicious_words else [],
                'timestamp': scan.timestamp.isoformat()
            })
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': f"Failed to fetch history: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
