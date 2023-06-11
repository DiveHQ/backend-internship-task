
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schema.user import TotalUsers, UserResponse, User, UserUpdate, UserUpdateResponse
from utils.utils import RoleChecker
from utils.user_utils import create_user, check_for_user, update_existing_user, delete_existing_user
from db import models
from datetime import datetime


manager_router = APIRouter(tags=["Manager"], prefix="/manager/users")
allow_operation = RoleChecker(["manager"])



@manager_router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=TotalUsers)
def get_users(db: Session = Depends(get_db)):

    """
    Returns all users with the user role
    Args:
        db: Database session
        
    Return: The users in the db with the user role

    """

    users = db.query(models.User).all()
    users_response = [UserResponse(id=user.id, 
                                   email=user.email, 
                                   first_name=user.first_name, 
                                   last_name=user.last_name, 
                                   role=user.role,
                                   expected_calories=user.expected_calories
                                   ) for user in users]
    return TotalUsers(total=len(users_response), data=users_response)

@manager_router.get("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    """
    Return a user with the specified id
    Args:
        user_id: The id of the user
        db: Database session
        
    Return: The user in the db

    """

    user = check_for_user(db, user_id).first()

    returned_user = UserResponse(id=user.id, 
                        email=user.email, 
                        first_name=user.first_name, 
                        last_name=user.last_name, 
                        role=user.role,
                        expected_calories=user.expected_calories)
    return returned_user

@manager_router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_operation)], response_model=UserResponse)
def create_new_user(user: User, db: Session = Depends(get_db)):

    """
    Creates a regular user
    Args:
        user: User schema that is accepted in request
        db: Database session

    Return: The newly created user 

    """

    user = create_user(user, db)

    return user


@manager_router.put('/{user_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)], response_model=UserUpdateResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Updates a regular user
    Args:
        user_id: The id of the user to be updated
        user: User schema that is accepted in request to update user details
        db: Database session

    Return: The newly updated user 

    """
    updated_user = update_existing_user(user_id, user, db)
    return updated_user

@manager_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_operation)])
def delete_user(user_id: int, db: Session = Depends(get_db)):

    """
    Deletes a regular user
    Args:
        user_id: The id of the user to be updated
        db: Database session

    Return: Nothing 

    """

    delete_existing_user(user_id, db)