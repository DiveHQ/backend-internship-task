from fastapi import FastAPI, Request, status
from src.core.response import APIResponse
from src.core.exceptions import ErrorResponse
from src.routes.auth import auth_router
from src.routes.calories import calorie_router
from src.db import models
from src.schema.user import User
from src.core.configvars import env_config
from src.db.models import Role
from src.utils.user_utils import create_new_user
from contextlib import asynccontextmanager
from src.db.database import SessionLocal
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from alembic import command
from alembic.config import Config
from src.db.database import engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy import inspect

def check_tables_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return bool(tables)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not check_tables_exist():
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
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
        user = db.query(models.User).filter_by(role="admin").first()
        if not user:
            create_new_user(admin, db)
    finally:
        db.close()

    yield
    db.close()

app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    res = APIResponse(
        data=[],
        errors=[error for error in exc.errors()],
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=res.to_dict(),
    )


async def http_exception_handler(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


@app.get("/")
async def root():
    return {"message": "Welcome to the Calories Input API"}


app.add_exception_handler(ErrorResponse, http_exception_handler)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(calorie_router, prefix="/api/v1")
