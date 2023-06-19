from flask import Flask
from api.database import db
from api.routes.entry_routes import entry_blueprint
from api.routes.user_routes import user_blueprint
from flask.blueprints import Blueprint
from config import Config
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(entry_blueprint, url_prefix='/api') 
    app.register_blueprint(user_blueprint, url_prefix='/api') 


    return app

app = create_app()
with app.app_context():
    db.create_all()
jwt = JWTManager()
jwt.init_app(app)


if __name__ == '__main__':
    app.run(debug = True)
