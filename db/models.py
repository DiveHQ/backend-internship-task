

from db.database import Base
from sqlalchemy import Column, String, Integer, Time, ForeignKey, Enum, Boolean, Date, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import enum

class Role(enum.Enum):
    user = "user"
    user_manager = "manager"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(Role), server_default=Role.user.name)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expected_calories = Column(Integer, nullable=False, server_default="1000")
    calorie_entries = relationship("CalorieEntry", back_populates="user")
