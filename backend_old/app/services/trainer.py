"""Model training service."""
import os
import json
import time
import logging
from datetime import datetime
from typing import Tuple, Dict, Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
import joblib

from app.services.preprocessing import preprocessor
from app.extensions import db
from app.models.prediction import ModelMetric

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and evaluates multiple ML models for phishing detection."""

    ALGORITHMS = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        "naive_bayes": MultinomialNB(),
        "random_forest": RandomForestClassifier(
            n_estimators=200, random_state=42, n_jobs=-1
        ),
        "svm": LinearSVC(random_state=42, dual=True),
    }

    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.vectorizer: TfidfVectorizer = None
        self.results: Dict[str, Dict[str, Any]] = {}

    def load_dataset(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("Dataset must have 'text' and 'label' columns")
        df["text"] = df["text"].astype(str).fillna("")
        df["label"] = df["label"].astype(str).str.lower().str.strip()
        df = df[df["label"].isin(["phishing", "legitimate", "spam", "ham"])]
        df["label"] = df["label"].replace({"spam": "phishing", "ham": "legitimate"})
        df = df.dropna(subset=["text", "label"])
        df = df[df["text"].str.strip() != ""]
        return df

    def preprocess_corpus(self, texts) -> list:
        return [preprocessor.preprocess(str(t)) for t in texts]

    def train_all(
        self,
        csv_path: str,
        test_size: float = 0.2,
        save_best: bool = True,
    ) -> Dict[str, Any]:
        logger.info("Loading dataset from %s", csv_path)
        df = self.load_dataset(csv_path)
        logger.info("Loaded %d samples", len(df))

        cleaned = self.preprocess_corpus(df["text"].values)

        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True,
        )
        X = self.vectorizer.fit_transform(cleaned)
        y = (df["label"].values == "phishing").astype(int)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        self.results = {}
        best_f1 = -1.0
        best_name = None
        best_model = None

        for name, model in self.ALGORITHMS.items():
            logger.info("Training %s...", name)
            start = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            cm = confusion_matrix(y_test, y_pred).tolist()
            report = classification_report(
                y_test, y_pred,
                target_names=["legitimate", "phishing"],
                output_dict=True,
                zero_division=0,
            )

            self.results[name] = {
                "model": model,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "confusion_matrix": cm,
                "classification_report": report,
                "training_time": train_time,
                "train_samples": int(X_train.shape[0]),
                "test_samples": int(X_test.shape[0]),
            }

            logger.info(
                "%s -> acc=%.4f prec=%.4f rec=%.4f f1=%.4f",
                name, accuracy, precision, recall, f1,
            )

            if f1 > best_f1:
                best_f1 = f1
                best_name = name
                best_model = model

        vectorizer_path = os.path.join(self.model_dir, "tfidf_vectorizer.joblib")
        joblib.dump(self.vectorizer, vectorizer_path)

        comparison = {
            "results": {
                name: {k: v for k, v in r.items() if k != "model"}
                for name, r in self.results.items()
            },
            "best_algorithm": best_name,
            "best_f1": best_f1,
        }

        metadata = {
            "best_algorithm": best_name,
            "best_f1": best_f1,
            "best_accuracy": self.results[best_name]["accuracy"],
            "best_precision": self.results[best_name]["precision"],
            "best_recall": self.results[best_name]["recall"],
            "trained_at": datetime.utcnow().isoformat(),
            "training_samples": int(X.shape[0]),
            "all_results": {
                name: {
                    "accuracy": r["accuracy"], "precision": r["precision"],
                    "recall": r["recall"], "f1_score": r["f1_score"],
                } for name, r in self.results.items()
            },
        }
        with open(os.path.join(self.model_dir, "model_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        if save_best and best_model is not None:
            joblib.dump(best_model, os.path.join(self.model_dir, "best_model.joblib"))
            joblib.dump(best_model, os.path.join(self.model_dir, f"{best_name}.joblib"))
            logger.info("Saved best model: %s (f1=%.4f)", best_name, best_f1)

        return comparison

    def persist_metrics_to_db(self) -> None:
        """Persist training results to the database."""
        if not self.results:
            return
        try:
            ModelMetric.query.update({ModelMetric.is_active: False})
            db.session.commit()

            for name, r in self.results.items():
                metric = ModelMetric(
                    algorithm=name,
                    accuracy=float(r["accuracy"]),
                    precision=float(r["precision"]),
                    recall=float(r["recall"]),
                    f1_score=float(r["f1_score"]),
                    training_samples=int(r["train_samples"]),
                    test_samples=int(r["test_samples"]),
                    training_time_seconds=float(r["training_time"]),
                    confusion_matrix=r["confusion_matrix"],
                    classification_report=r["classification_report"],
                    is_active=(name == max(
                        self.results, key=lambda k: self.results[k]["f1_score"]
                    )),
                )
                db.session.add(metric)
            db.session.commit()
        except Exception as exc:  # pragma: no cover
            logger.exception("Failed to persist metrics: %s", exc)
            db.session.rollback()
