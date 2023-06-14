from typing import List
from passlib.context import CryptContext
from fastapi import Depends, status
from src.db.models import User
from src.utils.oauth2 import get_current_user
from src.core.exceptions import ErrorResponse
from src.core.configvars import env_config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role.name not in self.allowed_roles:
            raise ErrorResponse(
                data=[],
                errors=[{"message": env_config.ERRORS.get("NOT_PERMITTED")}],
                status_code=status.HTTP_403_FORBIDDEN,
            )
