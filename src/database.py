from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_At = db.Column(db.DateTime, default=datetime.now())
    updated_At = db.Column(db.DateTime, onupdate=datetime.now())
    role = db.Column(db.String(20), nullable=False, default='regular user')
    calories = db.relationship('Calories', backref="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
         return f'User {self.username}'

class Calories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    meal = db.Column(db.Text(), nullable=False)
    calorie = db.Column(db.Integer())
    created_At = db.Column(db.DateTime, default=datetime.now())
    updated_At = db.Column(db.DateTime, onupdate=datetime.now())
    is_below_expected = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'Calorie {self.id}'
