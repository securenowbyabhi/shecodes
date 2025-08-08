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

    # Proper CORS setup
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Optional: Additional fallback to ensure headers are applied
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'https://shecodes-frontend-42cfc16f09b9.herokuapp.com'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    init_db(app)
    app.register_blueprint(auth_bp)

    return app
