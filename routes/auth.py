from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        phone=data.get("phone")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }), 200
