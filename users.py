from fastapi import APIRouter, Depends, HTTPException, Query, status
from schema import UserUpdate
from models import User, engine, Session
from fastapi.encoders import jsonable_encoder
from auth import token_manager
from werkzeug.security import generate_password_hash


users_routes = APIRouter(prefix="/api/v1.0", tags=["Users"])

session = Session(bind=engine)

#route to display all users
@users_routes.get("/all_users", status_code=status.HTTP_200_OK)
async def all_users(
    current_user: str = Depends(token_manager),
    page: int = Query(1, ge=1),  # Page number (default: 1)
    page_size: int = Query(10, ge=1, le=100)  # Page size (default: 10, maximum: 100)
):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if existing_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
        )

    total_users = session.query(User).count()

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Query the entries with pagination
    users = (
        session.query(User)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total_users": total_users,
        "page": page,
        "page_size": page_size,
        "users": jsonable_encoder(users),
    }


#route to update the user
@users_routes.put("/edit_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id:int, user:UserUpdate, current_user:str = Depends(token_manager)):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

    if existing_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
            )
    user_to_update = session.query(User).filter_by(id=id).first()
    user_to_update.email = user.email
    user_to_update.password = generate_password_hash(user.password)
    
    session.commit()
    return {"message":"User updated successfully"}

#route to delete the entry
@users_routes.delete("/delete_user/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id:int, current_user:str = Depends(token_manager)):
    existing_user = session.query(User).filter_by(email=current_user).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

    if existing_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission"
            )
    user_to_delete = session.query(User).filter_by(id=id).first()
    session.delete(user_to_delete)
    session.commit()
    return {"message":"User deleted successfully"}
