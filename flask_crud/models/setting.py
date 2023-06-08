from flask_crud import db
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

class Setting(db.Model):
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    expected_calories_per_day = Column(Integer, nullable=True)  # Can be null if not provided

    user = db.relationship('User', backref='settings')