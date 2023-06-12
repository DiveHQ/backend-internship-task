from sqlalchemy import Column, Text, String, Integer, create_engine, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime



engine = create_engine("sqlite:///mydb.sql", echo=True)
Base = declarative_base()
Session = sessionmaker()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(String)
    calories = Column(Integer)
    users_id = Column(Integer, ForeignKey("users.id"))
    is_below_expected_calories = Column(Boolean, default=False)

    