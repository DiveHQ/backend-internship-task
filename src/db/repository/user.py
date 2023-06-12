from sqlalchemy.orm import Session

from src.schema.user import User
from src.db.models import User


def save_user_in_db(user, db):
    """
    Creates and stores new user in database
    Args:
        user: The schema object
        db: Database session

    Return: The newly stored user
    """

    new_user = user.dict().copy()
    new_user.pop("password_confirmation")

    new_user = User(**new_user)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
