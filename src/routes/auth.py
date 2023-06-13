from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.user_utils import (
    create_new_user,
    get_a_user,
    get_all_users,
    update_existing_user,
    delete_existing_user,
)
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

    token, exp = get_access_token(str(user_data.id))

    timestamp = exp.timestamp()

    return Token(token=token, exp=timestamp, token_type="Bearer")


@auth_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_operation)],
    response_model=UserResponse,
)
def create_user(
    user: User, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    """
    Return a newly created user
    Args:
        user: The user details to create the user
        current_user: The current user object
        db: Database session

    Return: A user

    """
    get_user_role = current_user.role.name
    if get_user_role == "admin":
        if user.role.name == "admin":
            raise ForbiddenError(detail="You are not allowed to create an admin user")
    if get_user_role == "manager":
        if user.role and (user.role.name == "admin" or user.role.name == "manager"):
            raise ForbiddenError(
                detail="You are not allowed to create a user with this role"
            )

    user = create_new_user(user, db)
    return user


@auth_router.get(
    "/", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)]
)
def get_users(db: Session = Depends(get_db)):
    """
    Returns all users in the db
    Args:
        db: Database session

    Return: The users in the db

    """

    users = get_all_users(db)
    return users


@auth_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
    response_model=UserResponse,
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Return a user with the specified id
    Args:
        user_id: The id of the user
        db: Database session

    Return: The user in the db

    """

    user = get_a_user(db, user_id)
    return user


@auth_router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
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


@auth_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allow_operation)],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a regular user
    Args:
        user_id: The id of the user to be updated
        db: Database session

    Return: Nothing

    """

    delete_existing_user(user_id, db)


@auth_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def delete_user(db: Session = Depends(get_db)):
    """
    Deletes all users
    Args:
        db: Database session

    Return: Nothing

    """

    db.query(models.User).delete()
    db.commit()
