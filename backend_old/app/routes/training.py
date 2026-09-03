"""Training routes - admin functionality."""
import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.models.prediction import ModelMetric
from app.services.trainer import ModelTrainer
from app.services.model_loader import loader

training_bp = Blueprint("training", __name__)


def _require_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return None, (jsonify({"error": "Forbidden", "message": "Admin required"}), 403)
    return user, None


@training_bp.route("/train", methods=["POST"])
@jwt_required()
def train():
    _, err = _require_admin()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    csv_path = data.get("dataset_path") or os.path.join(
        os.path.dirname(current_app.config["ML_MODEL_PATH"]), "data", "phishing_dataset.csv"
    )
    test_size = float(data.get("test_size", 0.2))

    if not os.path.exists(csv_path):
        return jsonify({"error": "NotFound", "message": f"Dataset not found: {csv_path}"}), 404

    trainer = ModelTrainer(current_app.config["ML_MODEL_PATH"])
    try:
        comparison = trainer.train_all(csv_path, test_size=test_size)
        trainer.persist_metrics_to_db()
    except Exception as exc:
        return jsonify({"error": "TrainingError", "message": str(exc)}), 500

    loader.load(current_app.config["ML_MODEL_PATH"])

    return jsonify({
        "success": True,
        "message": "Training complete",
        "comparison": comparison,
    }), 200


@training_bp.route("/metrics", methods=["GET"])
@jwt_required()
def metrics():
    rows = ModelMetric.query.order_by(ModelMetric.created_at.desc()).limit(50).all()
    return jsonify({"success": True, "metrics": [m.to_dict() for m in rows]}), 200


@training_bp.route("/metrics/latest", methods=["GET"])
def metrics_latest():
    rows = (
        ModelMetric.query.order_by(ModelMetric.created_at.desc()).limit(4).all()
    )
    return jsonify({
        "success": True,
        "model_info": loader.info(),
        "metrics": [m.to_dict() for m in rows],
    }), 200


@training_bp.route("/activate/<int:metric_id>", methods=["POST"])
@jwt_required()
def activate(metric_id: int):
    user, err = _require_admin()
    if err:
        return err
    target = ModelMetric.query.get(metric_id)
    if not target:
        return jsonify({"error": "NotFound", "message": "metric not found"}), 404
    ModelMetric.query.update({ModelMetric.is_active: False})
    target.is_active = True
    db.session.commit()
    return jsonify({"success": True, "active": target.to_dict()}), 200
