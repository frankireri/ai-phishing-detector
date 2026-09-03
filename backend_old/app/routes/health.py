"""Health check endpoints."""
from flask import Blueprint, jsonify, current_app
from app.services.model_loader import loader

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "AI Phishing Detector API",
            "version": "1.0.0",
            "model_loaded": loader.is_ready(),
        }
    )


@health_bp.route("/info", methods=["GET"])
def info():
    return jsonify(
        {
            "service": "AI-Based Phishing Detection System",
            "institution": "Catholic University of Eastern Africa",
            "author": "Maximillian Saitabau",
            "version": "1.0.0",
            "model": loader.info(),
        }
    )
