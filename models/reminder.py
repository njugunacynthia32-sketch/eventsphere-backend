from models import db


class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    remind_at = db.Column(db.String(50))
    status = db.Column(db.String(30))
    method = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

    event = db.relationship(
        "Event",
        back_populates="reminders"
    )