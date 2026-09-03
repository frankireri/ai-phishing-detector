"""Flask application factory."""
import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import get_config
from app.extensions import db, migrate, jwt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(config_object=None):
    """Application factory pattern."""
    app = Flask(__name__)

    if config_object is None:
        config_object = get_config()
    app.config.from_object(config_object)

    os.makedirs(app.config["ML_MODEL_PATH"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["ALLOWED_ORIGINS"]}},
        supports_credentials=True,
    )

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[f"{app.config['RATE_LIMIT_PER_MINUTE']} per minute"],
        storage_uri="memory://",
    )

    from app.routes.auth import auth_bp
    from app.routes.predict import predict_bp
    from app.routes.training import training_bp
    from app.routes.analytics import analytics_bp
    from app.routes.health import health_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(predict_bp, url_prefix="/api/predict")
    app.register_blueprint(training_bp, url_prefix="/api/training")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    from app.errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        from app.models import user, prediction  # noqa: F401
        db.create_all()
        try:
            from app.services.model_loader import ensure_model_loaded
            ensure_model_loaded(app)
        except Exception as exc:
            logger.warning("Model preload skipped: %s", exc)

    return app
