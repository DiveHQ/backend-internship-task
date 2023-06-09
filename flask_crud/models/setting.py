from flask_crud import db
from sqlalchemy import Column, Integer, String,ForeignKey

import uuid

def generate_uuid():
    return str(uuid.uuid4())


class Setting(db.Model):
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    expected_calories_per_day = Column(Integer, nullable=True)  # Can be null if not provided

    user = db.relationship('User', backref='settings')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expected_calories_per_day': self.expected_calories_per_day,
        }