from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from models import db
from models.user import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone
    }), 200


@profile_bp.route("/", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    data = request.get_json()

    user.full_name = data.get("full_name", user.full_name)
    user.phone = data.get("phone", user.phone)

    if data.get("password"):
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200