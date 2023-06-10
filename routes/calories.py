
from fastapi import APIRouter, HTTPException, status, Depends
from utils.oauth2 import get_current_user
from schema.calories import CalorieEntryResponse, Calorie
from db.database import get_db
from sqlalchemy.orm import Session
from db import models

calorie_router = APIRouter(tags=["Calorie"], prefix="/calories")

def check_for_calorie(db, calorie_id, current_user):
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

@calorie_router.get("/", status_code=status.HTTP_200_OK, response_model=CalorieEntryResponse)
def get_all_calories(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    all_entries = db.query(models.CalorieEntry).filter(models.CalorieEntry.user_id == current_user.id).all() 
    return CalorieEntryResponse(total=len(all_entries), data=all_entries)

@calorie_router.get("/{calorie_id}", status_code=status.HTTP_200_OK, response_model=Calorie)
def get_calorie_entry(calorie_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    calorie_entry = check_for_calorie(db, calorie_id, current_user)
    return_data = calorie_entry.first()
    return Calorie(date=return_data.date, 
                   time=return_data.time, 
                   text=return_data.text, 
                   number_of_calories=return_data.number_of_calories,
                   user_id=current_user.id,
                   is_below_expected=return_data.is_below_expected)