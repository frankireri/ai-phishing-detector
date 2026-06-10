"""Prediction and model metric models."""
from datetime import datetime
from app.extensions import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    message_text = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), nullable=False, default="email")  # email | sms
    prediction = db.Column(db.String(20), nullable=False)  # phishing | legitimate
    confidence = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(100), nullable=False)
    suspicious_keywords = db.Column(db.JSON)
    processing_time_ms = db.Column(db.Float)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message_type": self.message_type,
            "prediction": self.prediction,
            "confidence": round(self.confidence, 4),
            "model_used": self.model_used,
            "suspicious_keywords": self.suspicious_keywords or [],
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ModelMetric(db.Model):
    __tablename__ = "model_metrics"

    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50), nullable=False, index=True)
    accuracy = db.Column(db.Float, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)
    training_samples = db.Column(db.Integer, nullable=False)
    test_samples = db.Column(db.Integer, nullable=False)
    training_time_seconds = db.Column(db.Float)
    confusion_matrix = db.Column(db.JSON)
    classification_report = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=False, nullable=False, index=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "algorithm": self.algorithm,
            "accuracy": round(self.accuracy, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
            "training_samples": self.training_samples,
            "test_samples": self.test_samples,
            "training_time_seconds": self.training_time_seconds,
            "confusion_matrix": self.confusion_matrix,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
