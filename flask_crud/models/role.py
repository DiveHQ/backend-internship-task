from sqlalchemy import Column, String
import uuid
from flask_crud import db

class Role(db.Model):
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)


    