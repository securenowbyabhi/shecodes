import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from .db import init_db
from .routes.auth_routes import auth_bp

def create_app():
    load_dotenv()

    # Point Flask to the React build directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    react_build = os.path.join(root_dir, "frontend", "build")

    app = Flask(__name__, static_folder=react_build, static_url_path="/")
    CORS(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    init_db(app)
    app.register_blueprint(auth_bp)

    # Serve React for non-API routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app
