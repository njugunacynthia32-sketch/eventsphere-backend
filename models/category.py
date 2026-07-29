from models import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(30))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    events = db.relationship(
        "Event",
        back_populates="category",
        cascade="all, delete-orphan"
    )