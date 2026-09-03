import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def train_model():
    print("Loading dataset...")
    # Load the dataset
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'phishing_dataset.csv')
    df = pd.read_csv(data_path)
    
    # The CSV has 'text' and 'label' columns
    X = df['text']
    y = df['label']
    
    # Convert text to TF-IDF features
    print("Extracting features with TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_features = vectorizer.fit_transform(X)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42)
    
    # Train the model (Random Forest is more robust)
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model trained successfully! Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    print("Saving model and vectorizer...")
    with open(os.path.join(os.path.dirname(__file__), 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
        
    with open(os.path.join(os.path.dirname(__file__), 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("Done! Model is ready for use.")

if __name__ == "__main__":
    train_model()
