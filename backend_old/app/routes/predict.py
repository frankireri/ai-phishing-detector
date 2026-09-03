"""Prediction routes - main functionality."""
import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.prediction import Prediction
from app.services.model_loader import loader
from app.utils.security import get_client_ip

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("", methods=["POST"])
def predict():
    """Public prediction endpoint (rate-limited by limiter)."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or data.get("message") or "").strip()
    message_type = (data.get("type") or "email").lower()
    if message_type not in ("email", "sms"):
        message_type = "email"

    if not text:
        return jsonify({"error": "BadRequest", "message": "text field is required"}), 400
    if len(text) > 50000:
        return jsonify({"error": "BadRequest", "message": "text too long (max 50000 chars)"}), 400

    if not loader.is_ready():
        return jsonify({"error": "ServiceUnavailable", "message": "Model not loaded"}), 503

    try:
        result = loader.predict(text)
    except Exception as exc:
        return jsonify({"error": "PredictionError", "message": str(exc)}), 500

    return jsonify(
        {
            "success": True,
            "result": {
                **result,
                "message_type": message_type,
                "input_length": len(text),
            },
        }
    ), 200


@predict_bp.route("/logged", methods=["POST"])
@jwt_required()
def predict_logged():
    """Authenticated prediction that also logs to DB."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or data.get("message") or "").strip()
    message_type = (data.get("type") or "email").lower()
    if message_type not in ("email", "sms"):
        message_type = "email"

    if not text:
        return jsonify({"error": "BadRequest", "message": "text field is required"}), 400

    if not loader.is_ready():
        return jsonify({"error": "ServiceUnavailable", "message": "Model not loaded"}), 503

    try:
        result = loader.predict(text)
    except Exception as exc:
        return jsonify({"error": "PredictionError", "message": str(exc)}), 500

    user_id = int(get_jwt_identity())
    record = Prediction(
        user_id=user_id,
        message_text=text[:10000],
        message_type=message_type,
        prediction=result["prediction"],
        confidence=result["confidence"],
        model_used=result["model_used"],
        suspicious_keywords=result["suspicious_keywords"],
        processing_time_ms=result["processing_time_ms"],
        ip_address=get_client_ip(request),
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({"success": True, "result": {**result, "message_type": message_type, "id": record.id}}), 201


@predict_bp.route("/batch", methods=["POST"])
def predict_batch():
    """Batch prediction endpoint."""
    data = request.get_json(silent=True) or {}
    messages = data.get("messages") or []
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "BadRequest", "message": "messages array required"}), 400
    if len(messages) > 100:
        return jsonify({"error": "BadRequest", "message": "max 100 messages per batch"}), 400

    if not loader.is_ready():
        return jsonify({"error": "ServiceUnavailable", "message": "Model not loaded"}), 503

    results = []
    for idx, item in enumerate(messages):
        if not isinstance(item, dict):
            results.append({"index": idx, "error": "invalid item"})
            continue
        text = (item.get("text") or "").strip()
        if not text:
            results.append({"index": idx, "error": "empty text"})
            continue
        try:
            results.append({"index": idx, "result": loader.predict(text)})
        except Exception as exc:
            results.append({"index": idx, "error": str(exc)})

    return jsonify({"success": True, "count": len(results), "results": results}), 200
