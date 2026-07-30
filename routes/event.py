from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.event import Event

event_bp = Blueprint("events", __name__)


@event_bp.route("/", methods=["GET"])
@jwt_required()
def get_events():
    events = Event.query.all()

    results = []

    for event in events:
        results.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "time": event.time,
            "location": event.location,
            "user_id": event.user_id,
            "category_id": event.category_id
        })

    return jsonify(results), 200


@event_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_event(id):
    event = Event.query.get_or_404(id)

    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "time": event.time,
        "location": event.location,
        "user_id": event.user_id,
        "category_id": event.category_id
    })


@event_bp.route("/", methods=["POST"])
@jwt_required()
def create_event():
    data = request.get_json()

    event = Event(
        title=data["title"],
        description=data.get("description"),
        date=data["date"],
        time=data["time"],
        location=data.get("location"),
        user_id=data["user_id"],
        category_id=data["category_id"]
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created successfully"}), 201


@event_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()

    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.date = data.get("date", event.date)
    event.time = data.get("time", event.time)
    event.location = data.get("location", event.location)

    db.session.commit()

    return jsonify({"message": "Event updated successfully"})


@event_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_event(id):
    event = Event.query.get_or_404(id)

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted successfully"})