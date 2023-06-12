from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_name = "sql_app.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
