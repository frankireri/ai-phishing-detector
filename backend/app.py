from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pickle
import os
import json
import subprocess

app = Flask(__name__)
# Enable CORS so the React frontend can communicate with this API
CORS(app)

# Configure Database connection (fallback to SQLite for easy local testing)
import traceback
try:
    # Try MySQL first
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/phishing_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
except:
    pass

# We will just use SQLite to guarantee it runs for the user immediately!
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'phishing_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret-key' # Change this in production
jwt = JWTManager(app)

db = SQLAlchemy(app)

# Define the Database Model for Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'

# Define the Database Model for Scan History
class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Optional user link
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
@jwt_required(optional=True)
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
    
    # Extract suspicious words if phishing (Using Random Forest Feature Importances)
    suspicious_words = []
    if prediction == 'phishing' and hasattr(model, 'feature_importances_'):
        feature_names = vectorizer.get_feature_names_out()
        importances = model.feature_importances_
        
        # Get the indices of the words present in the message
        feature_indices = features.nonzero()[1]
        
        # Create a list of (word, importance) for the present words
        word_weights = [(feature_names[idx], importances[idx]) for idx in feature_indices]
        
        # Sort by importance descending
        word_weights.sort(key=lambda x: x[1], reverse=True)
        
        # Get the top 5 most important words that are present in this phishing message
        suspicious_words = [word for word, weight in word_weights if weight > 0][:5]
    
    # Save to MariaDB
    try:
        current_user_id = get_jwt_identity()
        
        new_scan = ScanHistory(
            user_id=current_user_id,
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

@app.route('/report', methods=['POST'])
def report_feedback():
    data = request.get_json()
    if not data or 'text' not in data or 'correct_label' not in data:
        return jsonify({'error': 'Missing text or correct_label.'}), 400
        
    text = data['text']
    correct_label = data['correct_label']
    
    # In a real continuous learning system, we would save this to a Feedback table.
    # For now, we simply append it back to our training dataset!
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'phishing_dataset.csv')
        with open(data_path, 'a', encoding='utf-8') as f:
            # Escape quotes just in case
            safe_text = text.replace('"', '""')
            f.write(f'\n{correct_label},"{safe_text}"')
        return jsonify({'status': 'Feedback received and added to training queue!'})
    except Exception as e:
        return jsonify({'error': f"Failed to save feedback: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
@jwt_required(optional=True)
def get_history():
    try:
        current_user_id = get_jwt_identity()
        query = ScanHistory.query
        
        if current_user_id:
            query = query.filter_by(user_id=current_user_id)
            
        # Fetch the 10 most recent scans
        scans = query.order_by(ScanHistory.timestamp.desc()).limit(10).all()
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={'username': user.username, 'role': user.role}
        )
        return jsonify({'token': access_token, 'role': user.role}), 200
        
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/analytics', methods=['GET'])
@jwt_required()
def analytics():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
        
    total_users = User.query.count()
    total_scans = ScanHistory.query.count()
    phishing_scans = ScanHistory.query.filter_by(prediction='phishing').count()
    
    return jsonify({
        'total_users': total_users,
        'total_scans': total_scans,
        'phishing_scans': phishing_scans
    })

@app.route('/retrain', methods=['POST'])
@jwt_required()
def retrain():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
        
    try:
        train_script = os.path.join(os.path.dirname(__file__), 'train.py')
        subprocess.run(['python', train_script], check=True)
        
        # Reload model
        global model, vectorizer
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
            
        return jsonify({'message': 'Model retrained and reloaded successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to retrain model: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
