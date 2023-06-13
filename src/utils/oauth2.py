from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import models

from src.schema.user import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from src.core.configvars import env_config
from src.core.exceptions import CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"


def verify_token(token):
    """
    Verifies if a token is valid
    Raises an exception if the token is invalid
    Args:
        token: JWT encoded string

    Return: A token data that is the user's email

    """
    try:
        payload = jwt.decode(token, env_config.SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise CredentialsException(detail="Could not validate credentials")

        token_data: str = TokenData(id=user_id)

    except JWTError:
        raise CredentialsException(detail="Could not validate credentials")

    return token_data


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Creates an access token to be used by the user
    Args:
        data: A User object used to create the access token
        expires_delta: The time in seconds that the access token expires

    Return: An encoded JWT token

    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env_config.SECRET, algorithm=ALGORITHM)

    return encoded_jwt, expire


def get_access_token(sub: str):
    """
    Returns the created access token
    Args:
        sub: A string used to create the token

    Return: The created access token

    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, exp = create_access_token(
        {"sub": sub}, expires_delta=access_token_expires
    )
    return access_token, exp


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Returns the currently logged-in user
    Args:
        token: JWT encoded string
        db: A db session object

    Return: The user

    """
    token = verify_token(token)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    if not user:
        raise CredentialsException(detail="User not authenticated")
    return user
