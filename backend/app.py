from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
# Enable CORS so the React frontend can communicate with this API
CORS(app)

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
    
    return jsonify({
        'prediction': prediction,
        'confidence': round(confidence, 2),
        'suspicious_words': suspicious_words
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
