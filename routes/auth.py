

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from utils.utils import get_password_hash
from db import models
from db.database import get_db
from db.repository.user import create_new_user

from schema.user import User, Token, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils import verify_password
from utils.oauth2 import get_access_token
from core.exceptions import ValidationError, UserNotFoundError


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

    user_data = db.query(models.User).filter(models.User.email == user.email).first()
    if user_data:
        raise ValidationError(detail="User already exists")
    hash_passwd = get_password_hash(user.password)
    if user.password != user.password_confirmation:
        raise ValidationError(detail="Passwords do not match")

    user.password = hash_passwd
    new_user = create_new_user(user, db)
    return UserResponse(id=new_user.id, 
                        email=new_user.email, 
                        first_name=new_user.first_name, 
                        last_name=new_user.last_name, 
                        role=new_user.role,
                        expected_calories=new_user.expected_calories)


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
        raise UserNotFoundError(error_msg="Invalid Credentials")

    if not verify_password(user.password, user_data.password):
        raise ValidationError(error_msg="Invalid credentials")

    token = get_access_token(str(user_data.id))

    return Token(token=token, token_type="Bearer")