from src.db import models
from src.schema.user import (
    UserResponse,
    UserUpdate,
    UserUpdateResponse,
    UserPaginatedResponse,
)
from src.core.exceptions import UserAlreadyExistsError, ValidationError, ErrorResponse
from src.db.repository.user import save_user_in_db
from datetime import datetime
from src.core.exceptions import NotFoundError, ForbiddenError
from src.utils.utils import get_password_hash
from sqlalchemy import desc
from src.core.configvars import env_config
from fastapi import status


user_link = "/api/v1/users"


def check_for_user(db, user_id):
    """
    Checks for the existence of a user in the database
    Raises an error if the user with the id does not exist
    """
    user_in_db = db.query(models.User).filter(models.User.id == user_id)
    first_user = user_in_db.first()
    if not first_user:
        raise ErrorResponse(data=[], errors={"message": env_config.ERRORS.get("USER_NOT_FOUND")}, status_code=status.HTTP_404_NOT_FOUND)

    return user_in_db


def check_user_and_role(db, user_id, current_user, msg):
    user = check_for_user(db, user_id)
    first_user = user.first()

    if current_user.role.name == "admin":
        return user

    if current_user.role.name == "manager":
        if first_user.role.name != "user":
            raise ErrorResponse(data=[], errors={"message":msg}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return user

    if current_user.id != first_user.id:
        raise ErrorResponse(data=[], errors={"message":msg}, status_code=status.HTTP_403_FORBIDDEN)
        

    return user


def get_all_users(db, page, limit):
    """
    Returns all users
    Args:
        db: Database session

    Return: The users in the db

    """

    total_users = db.query(models.User).count()
    pages = (total_users - 1) // limit + 1
    offset = (page - 1) * limit
    users = (
        db.query(models.User)
        .order_by(desc(models.User.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )

    users_response = [
        UserResponse(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            expected_calories=user.expected_calories,
        )
        for user in users
    ]

    links = {
        "first": f"{user_link}?limit={limit}&page=1",
        "last": f"{user_link}?limit={limit}&page={pages}",
        "current_page": f"{user_link}?limit={limit}&page={page}",
        "next": None,
        "prev": None,
    }

    if page < pages:
        links["next"] = f"{user_link}?limit={limit}&page={page + 1}"

    if page > 1:
        links["prev"] = f"{user_link}?limit={limit}&page={page - 1}"

    return UserPaginatedResponse(
        total=total_users,
        page=page,
        total_pages=pages,
        users_response=users_response,
        links=links,
        size=limit,
    )


def get_a_user(db, user_id):
    """
    Return a user with the specified id
    Args:
        user_id: The id of the user
        db: Database session

    Return: The user in the db

    """

    user = check_for_user(db, user_id).first()

    returned_user = UserResponse(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        expected_calories=user.expected_calories,
    )
    return returned_user


def create_new_user(user, db):
    """
    Creates a regular user
    Args:
        user: User schema that is accepted in request
        db: Database session

    Return: The newly created user

    """

    user_data = db.query(models.User).filter(models.User.email == user.email).first()
    if user_data:
        raise ErrorResponse(data=[], errors={"message": env_config.ERRORS.get("USER_EXISTS")}, status_code=status.HTTP_409_CONFLICT)

    hash_passwd = get_password_hash(user.password)
    if user.password != user.password_confirmation:
        raise ErrorResponse(data=[], errors={"message": env_config.ERRORS.get("PASSWORD_MATCH_DETAIL")}, status_code=status.HTTP_400_BAD_REQUEST)

    user.password = hash_passwd

    new_user = save_user_in_db(user, db)

    return UserResponse(
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        expected_calories=new_user.expected_calories,
    )


def update_existing_user(user_id, user, db, current_user):
    """
    Updates a regular user
    Args:
        user_id: The id of the user to be updated
        user: User schema that is accepted in request to update user details
        db: Database session

    Return: The newly updated user

    """
    user_in_db = check_user_and_role(
        db, user_id, current_user, env_config.ERRORS.get("NOT_PERMITTED_UPDATE_USER")
    )
    current_time = datetime.utcnow()
    updated_user = UserUpdate(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        updated_at=current_time,
        role=user.role,
        expected_calories=user.expected_calories,
    )
    user_dict = updated_user.dict()
    new_update = {k: v for k, v in user_dict.items() if v is not None}

    user_in_db.update(new_update)
    db.commit()

    user = user_in_db.first()

    return UserUpdateResponse(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        expected_calories=user.expected_calories,
        updated_at=user.updated_at,
    )


def delete_existing_user(user_id, db):
    """
    Deletes a regular user
    Args:
        user_id: The id of the user to be updated
        db: Database session

    Return: Nothing

    """

    user_in_db = check_for_user(db, user_id)
    user_in_db.delete()
    db.commit()
