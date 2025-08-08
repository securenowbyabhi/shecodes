import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .db import init_db
from .routes.auth_routes import auth_bp

# Author : av42956 
# InIT_FILE : Initialize the FLASK, CORS  and DB

def create_app():
    load_dotenv()  # Load environment variables

    app = Flask(__name__)

    # Add this route:
    @app.route('/')
    def index():
        return "Backend API is running!"

    # Proper CORS setup
    CORS(app, resources={r"/*": {"origins": "https://shecodes-frontend-42cfc16f09b9.herokuapp.com"}})

    init_db(app)
    app.register_blueprint(auth_bp)

    return app
