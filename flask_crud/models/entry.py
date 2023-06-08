from flask_crud import db
from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

class Entry(db.Model):
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    text = Column(String(255), nullable=False)
    calories = Column(Integer, nullable=True)  # Can be null if not provided
    is_below_expected = Column(Boolean, default=False)

    user = db.relationship('User', backref='entries')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'time': self.time,
            'text': self.text,
            'calories': self.calories,
            'is_below_expected': self.is_below_expected,
        }