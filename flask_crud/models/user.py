from sqlalchemy import Column, String, ForeignKey
import uuid
from datetime import datetime, timedelta
import jwt
from flask_crud import db
from flask_crud.config import DevelopmentConfig

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)
    role_id = Column(String(36), ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', backref='users')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': {
                'id': self.role.id,
                'name': self.role.name
            } if self.role else None
        }
    def generate_auth_token(self, expires_in=3600):
        payload = {
            'user_id': self.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, DevelopmentConfig.JWT_SECRET_KEY, algorithm='HS256')