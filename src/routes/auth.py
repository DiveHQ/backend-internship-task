

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.user_utils import create_new_user
from src.db import models
from src.db.database import get_db
from src.schema.user import User, Token, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.utils import verify_password
from src.utils.oauth2 import get_access_token
from src.core.exceptions import ValidationError, UserNotFoundError


auth_router = APIRouter(tags=["Auth"], prefix="/users")

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup(user: User, db: Session = Depends(get_db)):
    
    """
    Creates a regular user
    Args:
        user: User schema that is accepted in request
        db: Database session

    Return: The newly created user 

    """

    user = create_new_user(user, db)
    return user


@auth_router.post('/login', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    """
    Creates a token for authorization
    Args:
        user: OAuth2PasswordRequestForm which accepts a username and a password
        db: Database session

    Return: A JWT Token

    """
    
    user_data = db.query(models.User).filter(models.User.email == user.username).first()
    if not user_data:
        raise UserNotFoundError(detail="Invalid Credentials")

    if not verify_password(user.password, user_data.password):
        raise ValidationError(detail="Invalid credentials")

    token = get_access_token(str(user_data.id))

    return Token(token=token, token_type="Bearer")