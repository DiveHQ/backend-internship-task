# app/api/models/entry.py

from api.database import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_satisfied = db.Column(db.Boolean, default=False)
    calories = db.Column(db.Integer)

    def __init__(self, user_id, text, is_satisfied=False, calories=None):
        self.user_id = user_id
        self.text = text
        self.is_satisfied = is_satisfied
        self.calories = calories
