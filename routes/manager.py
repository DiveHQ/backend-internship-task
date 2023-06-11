
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schema.user import TotalUsers, UserResponse, User, UserUpdate, UserUpdateResponse
from utils.oauth2 import get_current_user
from utils.utils import RoleChecker
from utils.user_utils import create_new_user, get_a_user, update_existing_user, delete_existing_user, get_all_users


manager_router = APIRouter(tags=["Manager"], prefix="/manager/users")
allow_operation = RoleChecker(["manager"])



@manager_router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=TotalUsers)
def get_users(db: Session = Depends(get_db)):

    """
    Returns all users
    Args:
        db: Database session
        
    Return: The users in the db

    """

    users = get_all_users(db)

    return users

@manager_router.get("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=UserResponse)
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

@manager_router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_operation)], response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):

    """
    Creates a regular user
    Args:
        user: User schema that is accepted in request
        db: Database session

    Return: The newly created user 

    """

    user = create_new_user(user, db)

    return user


@manager_router.put('/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=UserUpdateResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Updates a regular user
    Args:
        user_id: The id of the user to be updated
        user: User schema that is accepted in request to update user details
        db: Database session

    Return: The newly updated user 

    """
    updated_user = update_existing_user(user_id, user, db, current_user)
    return updated_user

@manager_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_operation)])
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    """
    Deletes a regular user
    Args:
        user_id: The id of the user to be updated
        db: Database session

    Return: Nothing 

    """

    delete_existing_user(user_id, db, current_user)