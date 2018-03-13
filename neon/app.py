from flask import Flask

from neon.auth.controllers import auth
from neon.admin.controllers import admin

from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import bcrypt, csrf, db


def create_app():
    app = Flask(__name__, static_url_path="/static")

    load_configurations(app)
    initialise_extensions(app)
    register_blueprints(app)
    configure_cli(app)

    return app


def load_configurations(app):
    app.config.from_object(DevelopmentConfig)


def initialise_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(admin)


def configure_cli(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
