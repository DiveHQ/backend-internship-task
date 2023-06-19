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
