"""Model loader and prediction service."""
import os
import json
import logging
import time
from threading import Lock
from typing import Tuple, List, Optional

import joblib
import numpy as np

from app.services.preprocessing import preprocessor

logger = logging.getLogger(__name__)


class ModelLoader:
    """Loads the trained model and exposes a predict API."""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metadata: dict = {}
        self.algorithm_name: str = "unknown"
        self._lock = Lock()

    def load(self, model_dir: str) -> bool:
        model_path = os.path.join(model_dir, "best_model.joblib")
        vec_path = os.path.join(model_dir, "tfidf_vectorizer.joblib")
        meta_path = os.path.join(model_dir, "model_metadata.json")

        if not (os.path.exists(model_path) and os.path.exists(vec_path)):
            logger.warning("Model artefacts not found in %s", model_dir)
            return False

        with self._lock:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vec_path)
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    self.metadata = json.load(f)
                self.algorithm_name = self.metadata.get("best_algorithm", "unknown")
            else:
                self.algorithm_name = "unknown"
                self.metadata = {}
        logger.info("Loaded model '%s' from %s", self.algorithm_name, model_dir)
        return True

    def is_ready(self) -> bool:
        return self.model is not None and self.vectorizer is not None

    def predict(self, text: str) -> dict:
        if not self.is_ready():
            raise RuntimeError("Model is not loaded")

        start = time.time()
        cleaned = preprocessor.preprocess(text)
        features = self.vectorizer.transform([cleaned])

        raw_pred = int(self.model.predict(features)[0])

        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(features)[0]
            classes = list(self.model.classes_)
            phishing_idx = classes.index(1) if 1 in classes else int(np.argmax(proba))
            confidence = float(proba[phishing_idx])
        elif hasattr(self.model, "decision_function"):
            decision = float(self.model.decision_function(features)[0])
            confidence = 1.0 / (1.0 + np.exp(-decision))
        else:
            confidence = 1.0

        prediction_label = "phishing" if raw_pred == 1 else "legitimate"

        suspicious = preprocessor.extract_suspicious_keywords(text)
        elapsed_ms = (time.time() - start) * 1000.0

        return {
            "prediction": prediction_label,
            "confidence": float(confidence),
            "model_used": self.algorithm_name,
            "suspicious_keywords": suspicious,
            "processing_time_ms": round(elapsed_ms, 2),
        }

    def info(self) -> dict:
        return {
            "loaded": self.is_ready(),
            "algorithm": self.algorithm_name,
            "metadata": self.metadata,
        }


loader = ModelLoader()


def ensure_model_loaded(app) -> bool:
    """Called on startup to ensure the model is loaded."""
    model_dir = app.config.get("ML_MODEL_PATH")
    if loader.is_ready():
        return True
    if loader.load(model_dir):
        return True

    logger.info("Training initial model from bundled dataset...")
    from app.services.trainer import ModelTrainer
    csv_path = os.path.join(
        os.path.dirname(model_dir), "data", "phishing_dataset.csv"
    )
    if not os.path.exists(csv_path):
        logger.error("Dataset not found at %s", csv_path)
        return False
    trainer = ModelTrainer(model_dir)
    trainer.train_all(csv_path)
    trainer.persist_metrics_to_db()
    return loader.load(model_dir)
