"""Authentication routes (register, login, profile)."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from email_validator import validate_email as ev_validate, EmailNotValidError

from app.extensions import db
from app.models.user import User
from app.utils.security import validate_password, validate_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""
    full_name = (data.get("full_name") or "").strip()

    if not email or not username or not password:
        return jsonify({"error": "BadRequest", "message": "email, username, password required"}), 400

    try:
        ev_validate(email, check_deliverability=False)
    except EmailNotValidError as exc:
        return jsonify({"error": "BadRequest", "message": str(exc)}), 400

    if not validate_email(email):
        return jsonify({"error": "BadRequest", "message": "Invalid email format"}), 400

    valid_pw, pw_msg = validate_password(password)
    if not valid_pw:
        return jsonify({"error": "BadRequest", "message": pw_msg}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Conflict", "message": "Email already registered"}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Conflict", "message": "Username already taken"}), 409

    user = User(email=email, username=username, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "User registered successfully", "token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    identifier = (data.get("email") or data.get("username") or "").strip().lower()
    password = data.get("password") or ""

    if not identifier or not password:
        return jsonify({"error": "BadRequest", "message": "credentials required"}), 400

    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401
    if not user.is_active:
        return jsonify({"error": "Forbidden", "message": "Account disabled"}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "NotFound", "message": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200
