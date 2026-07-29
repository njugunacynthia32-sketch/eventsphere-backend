from models import db
from models.attendance import attendance


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    location = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="events"
    )

    category = db.relationship(
        "Category",
        back_populates="events"
    )

    reminders = db.relationship(
        "Reminder",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    attendees = db.relationship(
        "User",
        secondary=attendance,
        back_populates="attending_events"
    )