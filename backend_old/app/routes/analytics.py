"""Analytics routes."""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from app.extensions import db
from app.models.prediction import Prediction, ModelMetric
from app.models.user import User

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "NotFound"}), 404

    is_admin = user.is_admin
    q = Prediction.query
    if not is_admin:
        q = q.filter(Prediction.user_id == user_id)

    total = q.count()
    phishing = q.filter(Prediction.prediction == "phishing").count()
    legitimate = q.filter(Prediction.prediction == "legitimate").count()
    avg_conf = q.with_entities(func.avg(Prediction.confidence)).scalar() or 0.0

    today = datetime.utcnow().date()
    days_q = q.filter(Prediction.created_at >= today - timedelta(days=6))
    by_day = (
        days_q.with_entities(
            func.date(Prediction.created_at).label("day"),
            Prediction.prediction,
            func.count(Prediction.id).label("n"),
        )
        .group_by("day", Prediction.prediction)
        .all()
    )

    daily = {}
    for d, pred, n in by_day:
        key = str(d)
        daily.setdefault(key, {"phishing": 0, "legitimate": 0})
        daily[key][pred] = n

    return jsonify({
        "success": True,
        "summary": {
            "total_predictions": total,
            "phishing_detected": phishing,
            "legitimate_detected": legitimate,
            "phishing_rate": round((phishing / total * 100) if total else 0.0, 2),
            "average_confidence": round(float(avg_conf), 4),
            "daily_breakdown": daily,
        }
    }), 200


@analytics_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "NotFound"}), 404

    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    q = Prediction.query.order_by(Prediction.created_at.desc())
    if not user.is_admin:
        q = q.filter(Prediction.user_id == user_id)

    paginated = q.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "success": True,
        "items": [p.to_dict() for p in paginated.items],
        "page": paginated.page,
        "pages": paginated.pages,
        "per_page": paginated.per_page,
        "total": paginated.total,
    }), 200


@analytics_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "NotFound"}), 404

    q = Prediction.query
    if not user.is_admin:
        q = q.filter(Prediction.user_id == user_id)

    total = q.count()
    phishing = q.filter(Prediction.prediction == "phishing").count()
    legitimate = total - phishing

    by_type = (
        q.with_entities(
            Prediction.message_type,
            Prediction.prediction,
            func.count(Prediction.id),
        )
        .group_by(Prediction.message_type, Prediction.prediction)
        .all()
    )
    type_breakdown = {}
    for mt, pred, n in by_type:
        type_breakdown.setdefault(mt, {"phishing": 0, "legitimate": 0})
        type_breakdown[mt][pred] = n

    metrics = (
        ModelMetric.query.filter_by(is_active=True)
        .order_by(ModelMetric.created_at.desc())
        .limit(4)
        .all()
    )

    return jsonify({
        "success": True,
        "dashboard": {
            "total_predictions": total,
            "phishing_count": phishing,
            "legitimate_count": legitimate,
            "phishing_rate": round((phishing / total * 100) if total else 0, 2),
            "type_breakdown": type_breakdown,
            "active_models": [m.to_dict() for m in metrics],
        }
    }), 200
