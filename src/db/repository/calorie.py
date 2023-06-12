from sqlalchemy.orm import Session

from src.schema.calories import Calorie
from src.db.models import CalorieEntry


def create_new_calorie_entry(calorie: Calorie, db: Session):
    """
    Creates and stores calorie in database
    Args:
        calorie: The calorie schema object
        db: Database session

    Return: The newly stored calorie entry
    """

    new_calorie = calorie.dict().copy()

    new_calorie = CalorieEntry(**new_calorie)

    db.add(new_calorie)
    db.commit()
    db.refresh(new_calorie)
    return new_calorie
