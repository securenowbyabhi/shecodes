import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .db import init_db
from .routes.auth_routes import auth_bp

def create_app():
    # Load .env only in non-production (Heroku uses config vars)
    if os.environ.get("FLASK_ENV") != "production":
        load_dotenv()

    # Point Flask to the React build directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    react_build = os.path.join(root_dir, "frontend", "build")

    app = Flask(__name__, static_folder=react_build, static_url_path="/")
    CORS(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # DB + blueprints (your API likely under /shecodes via the blueprint)
    init_db(app)
    app.register_blueprint(auth_bp)

    # Simple health check (handy on Heroku)
    @app.route("/api/health")
    def health():
        return jsonify({"ok": True})

    # Serve React for non-API routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        # If the requested file exists in the build, serve it
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        # If build/index.html exists, serve SPA entry
        index_path = os.path.join(app.static_folder, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, "index.html")
        # Fallback (first boot before build, or misconfig)
        return "Build not found. If on Heroku, ensure the root package.json runs the frontend build.", 503

    return app
