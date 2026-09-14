import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///s201.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_RESPONSE_BYTES=int(os.getenv("MAX_RESPONSE_BYTES", "65536")),
        REQUEST_TIMEOUT_SECONDS=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")),
    )
    if config:
        app.config.update(config)
    db.init_app(app)
    from .routes import api
    app.register_blueprint(api, url_prefix="/api")
    with app.app_context():
        db.create_all()
    @app.get("/health")
    def health():
        return {"status": "ok"}
    return app
