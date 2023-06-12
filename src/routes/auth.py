from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.user_utils import create_new_user, update_existing_user
from src.db import models
from src.db.database import get_db
from src.schema.user import User, Token, UserResponse, UserUpdate
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.utils import verify_password
from src.utils.oauth2 import get_access_token, get_current_user
from src.core.exceptions import ForbiddenError, InvalidCredentialError
from src.utils.utils import RoleChecker

auth_router = APIRouter(tags=["Auth"], prefix="/users")
allow_operation = RoleChecker(["manager", "admin"])

@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
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



@auth_router.post("/login", response_model=Token)
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
        raise InvalidCredentialError(detail="Invalid Credentials")

    if not verify_password(user.password, user_data.password):
        raise InvalidCredentialError(detail="Invalid credentials")

    token = get_access_token(str(user_data.id))

    return Token(token=token, token_type="Bearer")

@auth_router.post("/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_operation)],
    response_model=UserResponse,
)
def create_user(
    user: User, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    
    """
    Return a newl created user
    Args:
        user_id: The id of the user
        db: Database session

    Return: The user in the db

    """

    get_user_role = current_user.role.name
    if get_user_role == "admin":
        if user.role.name == "admin":
            raise ForbiddenError(detail="You are not allowed to create an admin user")
    if get_user_role == "manager":
        if user.role.name == "admin" or user.role.name == "manager":
            raise ForbiddenError(detail="You are not allowed to create a user with this role")
        
    user = create_new_user(user, db)
    return user

@auth_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    
    """
    Updates a regular user
    Args:
        user_id: The id of the user to be updated
        user: User schema that is accepted in request to update user details
        db: Database session
        current_user: The currently logged in user

    Return: The newly updated user

    """

    updated_user = update_existing_user(user_id, user, db, current_user)
    return updated_user

