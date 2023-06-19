# api.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import requests
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
CORS(app)

# Database Models
#These models define the structure of the database tables and the fields associated with each table. The User model represents user information, and the CalorieEntry model represents the entries for calorie tracking.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    expected_calories = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class CalorieEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    text = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    is_below_expected = db.Column(db.Boolean, default=False)

# Authentication Decorator

def authenticate(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'message': 'Authorization required'}), 401
            
            try:
                token = auth_header.split(' ')[1]
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                user_id = payload['user_id']
                user = User.query.get(user_id)
                if not user or user.role != role:
                    return jsonify({'message': 'Unauthorized'}), 401
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except (jwt.InvalidTokenError, IndexError):
                return jsonify({'message': 'Invalid token'}), 401
        return wrapper
    return decorator