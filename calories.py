from fastapi import HTTPException, status, Depends, APIRouter, Query
from auth import token_manager
from schema import EntryCreate, EntryUpdate
from models import User, Entry, engine, Session
import requests
from sqlalchemy import func
from datetime import date
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder





calories_routes = APIRouter(prefix="/api/v1.0", tags=["Calories"])

session = Session(bind=engine)


#route to create new calor entry
@calories_routes.post("/new_entry", status_code=status.HTTP_201_CREATED)
async def new_calory(
    entry: EntryCreate,
    current_user: str = Depends(token_manager),
    expected_calories: int = 2000  # Default expected calories per day
):
    try:
        if not entry.calories:
            response = requests.get(f"https://www.nutritionix.com/food/{entry.text}")
            if response.status_code == 200:
                try:
                    # Extract the calories information from the response
                    data = response.text
                    print(response.json)
                    start_index = data.find("Calories") + len("Calories")
                    end_index = data.find("% Daily Value*")
                    calories_text = data[start_index:end_index].strip()
                    entry.calories = int(calories_text)
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to parse response from the API",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to fetch calories from the API",
                )

        existing_user = session.query(User).filter_by(email=current_user).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

        if existing_user.role not in ["user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
            )

        new_entry = Entry(text=entry.text, calories=entry.calories, users_id=existing_user.id)
        session.add(new_entry)
        session.commit()

        # Calculate the total calories for the current day
        today = date.today()
        total_calories = (
            session.query(func.sum(Entry.calories))
            .filter(func.DATE(Entry.date) == today)
            .scalar()
        )

        # Determine if the total calories for the day are less than the expected calories
        is_below_expected_calorie = total_calories < expected_calories

        new_entry.is_below_expected_calories = is_below_expected_calorie
        session.commit()
        
        return {"message": "New entry created"}
    except HTTPException as e:
        raise e  # Re-raise the HTTPException
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

#route to display all calories entry
@calories_routes.get("/all_entries", status_code=status.HTTP_200_OK)
async def all_entries(
    current_user: str = Depends(token_manager),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if existing_user.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
        )

    total_entries = session.query(Entry).filter_by(users_id=existing_user.id).count()

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Query the entries with pagination
    entries = (
        session.query(Entry)
        .filter_by(users_id=existing_user.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total_entries": total_entries,
        "page": page,
        "page_size": page_size,
        "entries": jsonable_encoder(entries),
    }




#route to update the entry
@calories_routes.put("/edit_entry/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_entry(id:int, entry:EntryUpdate, current_user:str = Depends(token_manager)):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

    if existing_user.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
            )
    entry_to_update = session.query(Entry).filter_by(id=id, users_id=existing_user.id).first()
    entry_to_update.text = entry.text
    entry_to_update.calories = entry.calories
    session.commit()
    return {"message":"Entry updated successfully"}

#route to delete the entry
@calories_routes.delete("/delete_entry/{id}", status_code=status.HTTP_200_OK)
async def delete_entry(id:int, current_user:str = Depends(token_manager)):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

    if existing_user.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
            )
    entry_to_delete = session.query(Entry).filter_by(id=id, users_id=existing_user.id).first()
    session.delete(entry_to_delete)
    session.commit()
    return {"message":"Entry deleted successfully"}