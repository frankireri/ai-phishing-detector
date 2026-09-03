"""Training dataset model."""
from datetime import datetime
from app.extensions import db


class TrainingDataset(db.Model):
    __tablename__ = "training_datasets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    source = db.Column(db.String(150))  # e.g. Kaggle, UCI, manual
    num_samples = db.Column(db.Integer, default=0, nullable=False)
    num_phishing = db.Column(db.Integer, default=0, nullable=False)
    num_legitimate = db.Column(db.Integer, default=0, nullable=False)
    file_path = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "source": self.source,
            "num_samples": self.num_samples,
            "num_phishing": self.num_phishing,
            "num_legitimate": self.num_legitimate,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
