from sqlalchemy import Column, String
import uuid
from flask_crud import db

def generate_uuid():
    return str(uuid.uuid4())

class Role(db.Model):
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False, unique=True)


    