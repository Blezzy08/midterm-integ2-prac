from functools import wraps

from flask import g, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

ROLE_LEVELS = {"user": 1, "admin": 2}


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def require_role(required_role: str):
    if required_role not in ROLE_LEVELS:
        raise ValueError(f"Unknown role: {required_role}")

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            user_role = getattr(g, "user_role", None)
            if user_role is None:
                return jsonify({"error": "Authentication required"}), 401
            if user_role not in ROLE_LEVELS or ROLE_LEVELS[user_role] < ROLE_LEVELS[required_role]:
                return jsonify({"error": "Insufficient permissions"}), 403
            return view_func(*args, **kwargs)

        return wrapped

    return decorator