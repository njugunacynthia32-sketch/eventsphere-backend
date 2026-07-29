from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config import Config
from models import db

# Import models
from models.user import User
from models.event import Event
from models.category import Category
from models.reminder import Reminder

load_dotenv()

migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return {
            "message": "Welcome to EventSphere API",
            "status": "running"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    