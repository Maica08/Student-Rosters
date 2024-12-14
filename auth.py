from flask import Blueprint, jsonify, request
from functools import wraps
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

users = {
    "admin": {"password": "roster_admin", "role": "admin"},
    "teacher": {"password": "roster_teacher", "role": "teacher"},
    "student": {"password": "roster_student", "role": "student"}
}

def role_required(required_roles):
    """
    Decorator to enforce role-based access control.
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()  
        def wrapper(*args, **kwargs):
            claims = get_jwt()  
            user_role = claims.get("role")
            if user_role not in required_roles:
                return jsonify({"error": "Access forbidden: Insufficient role"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login endpoint to authenticate users and return a JWT token.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username, additional_claims={"role": user["role"]}, expires_delta=timedelta(hours=8))
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Example of a protected endpoint that requires a valid JWT token.
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {current_user}!"}), 200
