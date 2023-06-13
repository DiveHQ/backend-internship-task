from fastapi import Depends, FastAPI

from src.db.database import get_db
from src.routes.auth import auth_router
from src.routes.calories import calorie_router
from src.db import models
from src.schema.user import User
from src.core.configvars import env_config
from src.db.models import Role
from src.utils.user_utils import create_new_user
from contextlib import asynccontextmanager
from src.db.database import SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        admin = User(
            email=env_config.ADMIN_EMAIL,
            first_name=env_config.ADMIN_FIRST_NAME,
            last_name=env_config.ADMIN_LAST_NAME,
            password=env_config.PASSWORD,
            password_confirmation=env_config.PASSWORD_CONFIRMATION,
            role=Role.admin.name,
        )
        create_new_user(admin, db)
    finally:
        db.close()

    yield
    db.query(models.User).delete()
    db.query(models.CalorieEntry).delete()
    db.commit()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to the Calories Input API"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(calorie_router, prefix="/api/v1")
