
from api.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    calorie_perday = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, role, calorie_perday):
        self.username = username
        self.password = password
        self.role = role
        self.calorie_perday = calorie_perday
