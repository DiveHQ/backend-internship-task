from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_crud.config import DevelopmentConfig, TestingConfig


def create_app(config):
    app = Flask(__name__)
    if config == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config == 'testing':
        app.config.from_object(TestingConfig)
    init_db(app)
    return app

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
