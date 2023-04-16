import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    config_name = os.getenv('FLASK_CONFIG') or 'default'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

