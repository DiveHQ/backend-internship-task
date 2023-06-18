from flask import Flask, jsonify
import os
from src.auth import auth
from src.calorie import calorie
from src.database import db

def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI")
        )

    else:
        app.config.from_mapping(test_config)

    
    db.app = app
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(calorie)
    

    if __name__ == "__init__":
        app.run(debug=True)

    return app
