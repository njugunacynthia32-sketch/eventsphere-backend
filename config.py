import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "eventsphere-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///eventsphere.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "eventsphere-jwt-secret"
    )
    