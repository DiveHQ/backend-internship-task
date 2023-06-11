

from fastapi import APIRouter, HTTPException, status, Depends, Query
from utils.oauth2 import get_current_user
from datetime import datetime
from schema.calories import CalorieEntry, Calorie, CalorieEntryResponse, CaloriePaginatedResponse, CalorieUpdate
from db.repository.calorie import create_new_calorie_entry
from db.database import get_db
from sqlalchemy.orm import Session
from db import models
from service.nutrixion import get_nutrition_data
from sqlalchemy import func
from sqlalchemy import desc

calorie_router = APIRouter(tags=["Calorie"], prefix="/calories")

calorie_link = "/api/v1/calories"

def check_for_calorie(db, calorie_id, current_user):
    
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Calorie entry with id {calorie_id} not found"
        )
    if first_entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not authorized to access this",
        )
    
    return calorie_entry

@calorie_router.get("/", status_code=status.HTTP_200_OK)
def get_all_calories(limit:int = Query(default=1, ge=1), page: int = Query(default=1, ge=1), current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    """
    Returns all calorie entries that belong to the current user
    Args:
        current_user: The current user object
        db: Database session
        
    Return: All calorie entries that corresponding to the CalorieEntryResponse model

    """

    total_calorie_entries = db.query(models.CalorieEntry).count()
    pages = (total_calorie_entries - 1) // limit + 1
    offset = (page - 1) * limit
    calorie_entries = db.query(
                        models.CalorieEntry).filter(
                        models.CalorieEntry.user_id == current_user.id
                        ).order_by(desc(
                        models.CalorieEntry.created_at)
                        ).offset(offset).limit(limit).all()
    
    print(type(calorie_entries[0]))
    calories_response = [Calorie(date=calorie.date,
                                 time=calorie.time,
                                 text=calorie.text,
                                 number_of_calories=calorie.number_of_calories,
                                 user_id=calorie.user_id,
                                 is_below_expected=calorie.is_below_expected) for calorie in calorie_entries]

    links = {
        "first": f"{calorie_link}?limit={limit}&page=1",
        "last": f"{calorie_link}?limit={limit}&page={pages}",
        "current_page": f"{calorie_link}?limit={limit}&page={page}",
        "next": None,
        "prev": None,
    }

    if page < pages:
        links["next"] = f"{calorie_link}?limit={limit}&page={page + 1}"

    if page > 1:
        links["prev"] = f"{calorie_link}?limit={limit}&page={page - 1}"

    return CaloriePaginatedResponse(
        calorie_entries=calories_response,
        total=total_calorie_entries,
        page=page,
        size=limit,
        pages=pages,
        links=links
    )

@calorie_router.get("/{calorie_id}", status_code=status.HTTP_200_OK, response_model=Calorie)
def get_calorie_entry(calorie_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    """
    Returns the calorie entry with the specified id
    Args:
        calorie_id: The id of the calorie entry to access from db
        current_user: The current user object
        db: Database session
        
    Return: The calorie entry that corresponds to the Calorie model

    """

    calorie_entry = check_for_calorie(db, calorie_id, current_user)
    return_data = calorie_entry.first()
    return Calorie(date=return_data.date, 
                   time=return_data.time, 
                   text=return_data.text, 
                   number_of_calories=return_data.number_of_calories,
                   user_id=current_user.id,
                   is_below_expected=return_data.is_below_expected)

@calorie_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Calorie)
def create_calorie(calorie_entry: CalorieEntry, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    """
    Creates a new calorie entry
    Args:
        calories_entry: Details of the calorie entry to save
        current_user: The current user object
        db: Database session

    Return: A new calorie entry that corresponds to the Calorie model

    """

    nf_calories=0
    date = datetime.now().date()
    time = datetime.now().time().strftime("%H:%M:%S")

    total_calories_today = db.query(
        func.coalesce(func.sum(models.CalorieEntry.number_of_calories), 0)
        ).filter(models.CalorieEntry.user_id == current_user.id and models.CalorieEntry.date == date
        ).scalar()


    if calorie_entry.number_of_calories is None:
        nf_calories = get_nutrition_data(calorie_entry.text)
    
    number_of_calories = nf_calories or calorie_entry.number_of_calories

    is_below_expected = (total_calories_today + number_of_calories) < current_user.expected_calories
    
    calorie = Calorie(
                    date=date, 
                    time=time, 
                    text=calorie_entry.text, 
                    number_of_calories=number_of_calories, 
                    user_id=current_user.id,
                    is_below_expected=is_below_expected)

    new_calorie_entry = create_new_calorie_entry(calorie, db)

    return Calorie(
                    date=new_calorie_entry.date, 
                    time=new_calorie_entry.time, 
                    text=new_calorie_entry.text, 
                    number_of_calories=new_calorie_entry.number_of_calories, 
                    user_id=new_calorie_entry.user_id,
                    is_below_expected=new_calorie_entry.is_below_expected)


@calorie_router.put("/{calorie_id}", status_code=status.HTTP_200_OK, response_model=Calorie)
def update_calorie(calorie_id: int, calorie_entry: CalorieUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    """
    Update a calorie entry
    Args:
        calorie_id: The id of the calorie entry to update
        calorie_entry: The new details to update the calorie entry in the db
        db: Database session
        current_user: The current user object

    Return: The updated calorie entry

    """

    calorie = check_for_calorie(db, calorie_id, current_user)
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

    return Calorie(date=updated_calorie_entry.date, 
                   time=updated_calorie_entry.time, 
                   text=updated_calorie_entry.text, 
                   number_of_calories=updated_calorie_entry.number_of_calories,
                   user_id=updated_calorie_entry.user_id,
                   is_below_expected=updated_calorie_entry.is_below_expected)


@calorie_router.delete("/{calorie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calorie(calorie_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    """
    Delete a calorie entry
    Args:
        calorie_id: The id of the calorie entry to update
        db: Database session
        current_user: The current user object

    Return: Nothing

    """

    calorie = check_for_calorie(db, calorie_id, current_user)
    calorie.delete()
    db.commit()