from flask import Blueprint, jsonify, request
from functools import wraps
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt

auth_bp = Blueprint("auth", __name__)

users = {
    "admin": {"password": "roster_admin", "role": "admin"},
    "teacher": {"password": "roster_teacher", "role": "teacher"},
    "student": {"password": "roster_student", "role": "student"}
}

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in required_roles:
                return jsonify({"error": "Access forbidden: Insufficient role"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity={"username": username, "role": user["role"]})
    return jsonify({"access_token": access_token}), 200