
from db import models
from sqlalchemy.orm import Session
from db.database import get_db
from schema.user import User, UserResponse, UserUpdate, UserUpdateResponse
from core.exceptions import ValidationError
from db.repository.user import create_new_user
from datetime import datetime
from core.exceptions import NotFoundError, ForbiddenError
from fastapi import Depends
from utils.utils import get_password_hash

def check_for_user(db, user_id):
    """
        Checks for the existence of a user in the database 
        Raises an error if the user with the id does not exist
    """
    user_in_db = db.query(models.User).filter(models.User.id == user_id)
    first_user = user_in_db.first()
    if not first_user:
        raise NotFoundError(detail=f"User with id {user_id} does not exist")

    return user_in_db

def check_user_and_role(db, user_id, msg):
    user = check_for_user(db, user_id)
    first_user = user.first()

    if first_user.role.name != "user":
        raise ForbiddenError(detail=msg)

    return user



def create_user(user: User, db: Session = Depends(get_db)):
   
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


def update_existing_user(user_id, user, db):
    """
    Updates a regular user
    Args:
        user_id: The id of the user to be updated
        user: User schema that is accepted in request to update user details
        db: Database session

    Return: The newly updated user 

    """
    user_in_db = check_user_and_role(db, user_id, "You do not have the permission to update this user")
    current_time = datetime.utcnow()
    updated_user = UserUpdate(email=user.email, 
                              first_name=user.first_name, 
                              last_name=user.last_name,
                              updated_at=current_time)
    user_dict = updated_user.dict()
    new_update = {k:v for k,v in user_dict.items() if v is not None}

    user_in_db.update(new_update)
    db.commit()

    user = user_in_db.first()


    return UserUpdateResponse(id=user.id, 
                        email=user.email, 
                        first_name=user.first_name, 
                        last_name=user.last_name, 
                        role=user.role, 
                        expected_calories=user.expected_calories,
                        updated_at=user.updated_at)


def delete_existing_user(user_id, db):
    """
    Deletes a regular user
    Args:
        user_id: The id of the user to be updated
        db: Database session

    Return: Nothing 

    """

    user_in_db = check_user_and_role(db, user_id, "You do not have the permission to delete this user")
    user_in_db.delete()
    db.commit()