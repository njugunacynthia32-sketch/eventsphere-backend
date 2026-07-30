from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db
from models.category import Category

category_bp = Blueprint("categories", __name__)


@category_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name,
            "color": category.color,
            "description": category.description
        }
        for category in categories
    ]), 200


@category_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()

    category = Category(
        name=data["name"],
        color=data.get("color"),
        description=data.get("description")
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully",
        "id": category.id
    }), 201