
from core.exceptions import NotFoundError, ForbiddenError
from db import models
from schema.calories import CalorieUpdate, CalorieResponse
from datetime import datetime

# def check_for_calorie_entry(db, calorie_id):
#     calorie = db.query(models.CalorieEntry).filter(models.CalorieEntry.id == calorie_id)
#     calorie_first = calorie.first()
#     if not calorie_first:
#         raise NotFoundError(detail=f"Calorie entry with id {calorie_id} does not exist")

#     return calorie

def check_for_calorie_and_owner(db, calorie_id, current_user):
    
    """
    Checks if a calorie entry exists and also if the calorie entry belongs to the current user
    Args:
        db: Database session
        calorie_id: The id of the calorie entry to obtain from db
        current_user: The current user object

    Return: The query object

    """

    calorie_entry = db.query(models.CalorieEntry).filter(models.CalorieEntry.id == calorie_id)
    first_entry = calorie_entry.first()
    if not first_entry:
        raise NotFoundError(
            detail=f"Calorie entry with id {calorie_id} not found"
        )
    if current_user.role.name == "admin":
        return calorie_entry
    elif first_entry.user_id != current_user.id:
            raise ForbiddenError(
                detail="You not authorized to access this",
            )
    
    return calorie_entry

def update_calorie_entry(calorie_id, calorie_entry, db, current_user):
    calorie = check_for_calorie_and_owner(db, calorie_id, current_user)
    current_time = datetime.utcnow()
    updated_calorie = CalorieUpdate(
                        text=calorie_entry.text,
                        number_of_calories=calorie_entry.number_of_calories,
                        is_below_expected=calorie_entry.is_below_expected,
                        updated_at=current_time
                    )
    updated_dict = updated_calorie.dict()
    new_update = {k:v for k,v in updated_dict.items() if v is not None}

    calorie.update(new_update)
    db.commit()
    updated_calorie_entry = calorie.first()

    return CalorieResponse(id=updated_calorie_entry.id,
                   date=updated_calorie_entry.date, 
                   time=updated_calorie_entry.time, 
                   text=updated_calorie_entry.text, 
                   number_of_calories=updated_calorie_entry.number_of_calories,
                   user_id=updated_calorie_entry.user_id,
                   is_below_expected=updated_calorie_entry.is_below_expected)

def delete_calorie_entry(db, calorie_id, current_user):

    """
    Deletes a calorie entry
    Args:
        db: Database session
        calorie_id: The id of the calorie entry to obtain from db
        current_user: The current user object

    Return: Nothing

    """

    calorie = check_for_calorie_and_owner(db, calorie_id, current_user)
    calorie.delete()
    db.commit()