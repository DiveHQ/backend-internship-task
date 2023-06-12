from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import models
from src.schema.user import AdminUserUpdate, UserWithRole
from src.utils.oauth2 import get_current_user
from src.utils.user_utils import (
    delete_existing_user,
    get_a_user,
    get_all_users,
    create_new_user,
    update_existing_user,
)

from src.utils.utils import RoleChecker

admin_user_router = APIRouter(tags=["Admin"], prefix="/admin/users")

allow_operation = RoleChecker(["admin"])


@admin_user_router.get(
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


@admin_user_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
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


@admin_user_router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_operation)]
)
def create_user(user: UserWithRole, db: Session = Depends(get_db)):
    """
    Return a user with the specified id
    Args:
        user_id: The id of the user
        db: Database session

    Return: The user in the db

    """

    user = create_new_user(user, db)
    return user


@admin_user_router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
)
def update_user(
    user_id: int,
    user: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_user = update_existing_user(user_id, user, db, current_user)
    return updated_user


@admin_user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allow_operation)],
)
def delete_user(
    user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    delete_existing_user(user_id, db, current_user)


@admin_user_router.delete(
    "/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_operation)]
)
def delete_user(db: Session = Depends(get_db)):
    db.query(models.User).delete()
    db.commit()
