from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    required_fields = ["full_name", "email", "password"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({
            "message": "Full name, email and password are required"
        }), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "message": "Email already exists"
        }), 400

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        phone=data.get("phone")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    user = User.query.filter_by(
        email=data.get("email")
    ).first()

    if not user or not check_password_hash(
        user.password,
        data.get("password", "")
    ):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}

    email = data.get("email")

    if not email:
        return jsonify({
            "message": "Email is required"
        }), 400

    user = User.query.filter_by(email=email).first()

    # We deliberately return the same response whether the account
    # exists or not, so the endpoint doesn't reveal registered emails.
    if not user:
        return jsonify({
            "message": "If an account exists, a password reset link has been generated."
        }), 200

    reset_token = create_access_token(
        identity=str(user.id),
        additional_claims={"reset": True}
    )

    return jsonify({
        "message": "Password reset token generated",
        "reset_token": reset_token
    }), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    from flask_jwt_extended import decode_token

    data = request.get_json() or {}

    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({
            "message": "Token and new password are required"
        }), 400

    try:
        decoded = decode_token(token)

        if not decoded.get("reset"):
            return jsonify({
                "message": "Invalid password reset token"
            }), 401

        user_id = decoded["sub"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        user.password = generate_password_hash(new_password)

        db.session.commit()

        return jsonify({
            "message": "Password reset successful"
        }), 200

    except Exception:
        return jsonify({
            "message": "Invalid or expired reset token"
        }), 401