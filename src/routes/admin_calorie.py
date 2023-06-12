from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.core.exceptions import NotFoundError
from src.db import models
from src.db.database import get_db
from src.utils.calorie_utils import update_calorie_entry
from src.utils.oauth2 import get_current_user
from src.utils.utils import RoleChecker
from src.schema.calories import CalorieUpdate
from src.utils.calorie_utils import delete_calorie_entry

admin_calorie_router = APIRouter(tags=["Admin"], prefix="/admin/calories")

allow_operation = RoleChecker(["admin"])


@admin_calorie_router.get(
    "/", status_code=status.HTTP_200_OK, dependencies=[Depends(allow_operation)]
)
def get_all_calories(db: Session = Depends(get_db)):
    """
    Returns all calories in the db
    Args:
        db: Database session

    Return: The calorie entries in the db

    """

    calorie_entry = db.query(models.CalorieEntry).all()
    return {"total": len(calorie_entry), "data": calorie_entry}


@admin_calorie_router.get(
    "/{calorie_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
)
def get_calorie(calorie_id: int, db: Session = Depends(get_db)):
    """
    Returns a calorie entry with the specified id
    Args:
        calorie_id: The id of the calorie
        db: Database session

    Return: The calorie entry

    """

    calorie_entry = (
        db.query(models.CalorieEntry)
        .filter(models.CalorieEntry.id == calorie_id)
        .first()
    )
    if not calorie_entry:
        raise NotFoundError(detail=f"Calorie Entry with id {calorie_id} does not exist")
    return calorie_entry


# @admin_calorie_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_operation)])
# def create_calorie_for_user():
#     pass


@admin_calorie_router.put(
    "/{calorie_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(allow_operation)],
)
def update_calorie(
    calorie_id: int,
    calorie_entry: CalorieUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Updates a calorie entry with the specified id
    Args:
        calorie_id: The id of the calorie entry to update
        calorie_entry: The new details to update the calorie entry in the db
        db: Database session
        current_user: The current user object

    Return: The calorie entry

    """

    calorie = update_calorie_entry(calorie_id, calorie_entry, db, current_user)

    return calorie


@admin_calorie_router.delete(
    "/{calorie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allow_operation)],
)
def delete_calorie(
    calorie_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Deletes a calorie entry with the specified id
    Args:
        calorie_id: The id of the calorie entry to update
        db: Database session

    Return: Nothing

    """

    delete_calorie_entry(db, calorie_id, current_user)


@admin_calorie_router.delete(
    "/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_operation)]
)
def delete_all_calories(db: Session = Depends(get_db)):
    """
    Deletes all calorie entries
    Args:
        db: Database session

    Return: Nothing

    """

    db.query(models.CalorieEntry).delete()
    db.commit()
