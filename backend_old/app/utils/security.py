"""Utility helpers."""
import re
from datetime import datetime


def validate_email(email: str) -> bool:
    pattern = r"^[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple:
    """Return (is_valid, message)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    return True, "Password is strong"


def get_client_ip(request) -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr or "0.0.0.0")
