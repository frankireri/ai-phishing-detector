"""Global error handlers."""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        return (
            jsonify(
                {
                    "error": exc.name,
                    "message": exc.description,
                    "status": exc.code,
                }
            ),
            exc.code,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_db_exception(exc):
        logger.exception("Database error: %s", exc)
        return (
            jsonify(
                {
                    "error": "DatabaseError",
                    "message": "A database error occurred. Please try again.",
                    "status": 500,
                }
            ),
            500,
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(exc):
        logger.exception("Unhandled exception: %s", exc)
        return (
            jsonify(
                {
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred.",
                    "status": 500,
                }
            ),
            500,
        )
