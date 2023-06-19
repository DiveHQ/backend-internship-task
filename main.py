"""_summary_
References:
Nutritionix API Documentation =  https://gist.github.com/mattsilv/6d19997bbdd02cf5337e9d4806b4f464
    
"""

# Import all the libraries and packages in the code
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi import FastAPI
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from enum import Enum
from passlib.context import CryptContext
from starlette.responses import Response
from pydantic import BaseModel
import datetime
from typing import Optional
import requests

# Setting  the debugging mode on
logging.basicConfig(level=logging.DEBUG)

# Setting the FastAPI 
app = FastAPI()

# Mount the static files which would contains the HTML files for testing the APIs
# app.mount("/static", StaticFiles(directory="static"), name="static")


headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://trackapi.nutritionix.com/docs/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# Added multiple origins to remove the cors errors which we may encounter later

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:8000/api",
]

# Setting up the parth for the SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///calories.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Middleware to pass on the cors error and to check the credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to interact with the database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define three roles for user, manager and an admin
class Role(str, Enum):
    USER = "user"
    USER_MANAGER = "user_manager"
    ADMIN = "admin"

# Defining the schema for the users.
''' It will contain the username, password, role, daily calorie goad, and the entries. The id will be genrated automatically'''
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    daily_calorie_goal = Column(Integer, nullable=False)
    entries = relationship('Entry', back_populates='user')

# Defining the schema for the entries.

''' The entries should contain the user id, date , time , the text whixh contains the food, calories, whether it is below the goal and the user.'''

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    text = Column(String(100), nullable=False)
    calories = Column(Integer)
    is_below_goal = Column(Boolean)
    user = relationship('User', back_populates='entries')

# The following code is used for database schema creation  and configuration. It will handle authentication as well as password hasing.
Base.metadata.create_all(bind=engine)
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to genrerate the hash function
def get_password_hash(password):
    return pwd_context.hash(password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    db = SessionLocal()
    user = db.query(User).filter_by(username=credentials.username).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return user

# Creating the model for the user
class UserLogin(BaseModel):
    username: str
    password: str

class EntryUpdate(BaseModel):
    date: datetime.date
    time: datetime.time
    text: str
    calories: int

class EntryCreate(BaseModel):
    date: datetime.date
    time: datetime.time
    text: str
    calories: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role
    daily_calorie_goal: int

# API to access the index page of the web application
@app.get("/")
async def index():
    response = Response(content="Hello, World!", media_type="text/plain")
    return response

# API to register the user
@app.post("/api/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        role=user.role.value,
        daily_calorie_goal=user.daily_calorie_goal
    )
    db.add(db_user)
    db.commit()
    # Return the status code and the success message.
    return {"status_code": 202, "message": "User registered successfully"}

# API to login 
@app.post("/api/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return {"message": "Login successful"}

# API to get all the entries of the user
@app.get("/api/entries")
async def get_entries(user: User = Depends(authenticate_user), db: Session = Depends(get_db)):
    if user.role == "admin":
        entries = db.query(Entry).all()
    elif user.role == "user_manager":
        entries = db.query(Entry).join(User).all()
    else:
        entries = db.query(Entry).filter_by(user_id=user.id).all()
    return entries

# API to post entries 
@app.post("/api/entries")
async def create_entry(entry: EntryCreate, user: User = Depends(authenticate_user), db: Session = Depends(get_db)):
    if not entry.calories:
        calories = fetch_calories_from_api(entry.text)
        if calories is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to fetch calories for the entered meal")
        entry.calories = calories
    total_calories = get_total_calories_for_day(user, entry.date)
    if not total_calories:
        total_calories = 0
    is_below_goal = total_calories + entry.calories < user.daily_calorie_goal

    db_entry = Entry(
        user_id=user.id,
        date=entry.date,
        time=entry.time,
        text=entry.text,
        calories=entry.calories,
        is_below_goal=is_below_goal
    )
    db.add(db_entry)
    db.commit()
    return {"message": "Entry created successfully"}

# Fetch calories from the api available 
def fetch_calories_from_api(meal_text):
    data = {"password": "Drive^&*", "email": "asifrahaman162@gmail.com"}
    response = requests.post('https://trackapi.nutritionix.com/v2/auth/signin', headers=headers, data=data)
    user_jwt = response.json()["x-user-jwt"]
    app_id = "effeff0e"
    app_key = "a26584f64a498f2f641bb6034dded946"
    headers.update( {
        "x-app-id": app_id, "x-app-key": app_key, "x-user-jwt":  user_jwt, 
    })
    params = {
        'query': meal_text,
        'self': 'true',
        'branded': 'true',
        'branded_food_name_only': 'false',
        'common': 'true',
        'common_general': 'true',
        'common_grocery': 'true',
        'common_restaurant': 'true',
        'detailed': 'false',
        'claims': 'false',
        'taxonomy': 'false',
    }
    response = requests.get('https://trackapi.nutritionix.com/v2/search/instant', params=params, headers=headers)
    if response.status_code == 200:
        
        response_json = response.json()
        if "branded" not in response_json or not response_json["branded"]:
            return 
        return int(response.json()["branded"][-1].get('nf_calories'))

# Get the details of the entry through the ID
@app.get("/api/entries/{entry_id}")
async def get_entry(entry_id: int, user: User = Depends(authenticate_user), db: Session = Depends(get_db)):
    # Check if the entry exists
    db_entry = db.query(Entry).filter_by(id=entry_id, user_id=user.id).first()
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    # Return the entry
    return {
        "id": db_entry.id,
        "user_id": db_entry.user_id,
        "date": db_entry.date,
        "time": db_entry.time,
        "text": db_entry.text,
        "calories": db_entry.calories,
        "is_below_goal": db_entry.is_below_goal
    }

# API to update the entry by ID
@app.put("/api/entries/{entry_id}")
async def update_entry(entry_id: int, entry: EntryUpdate, user: User = Depends(authenticate_user), db: Session = Depends(get_db)):
    # Check if the entry exists
    db_entry = db.query(Entry).filter_by(id=entry_id, user_id=user.id).first()
    if not db_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    # Update the entry with the provided data
    db_entry.date = entry.date
    db_entry.time = entry.time
    db_entry.text = entry.text
    db_entry.calories = entry.calories

    # Recalculate is_below_goal
    total_calories = get_total_calories_for_day(user, db_entry.date)
    is_below_goal = total_calories + entry.calories < user.daily_calorie_goal
    db_entry.is_below_goal = is_below_goal

    db.commit()

    return {"message": "Entry updated successfully"}

# Function to calcualate the total calories of the user per day
def get_total_calories_for_day(user, date):
    db = SessionLocal()
    total_calories = db.query(func.sum(Entry.calories)).filter_by(user_id=user.id, date=date).scalar()
    return total_calories

# Update the entries of of the food
@app.put("/api/entries/{entry_id}")
async def update_entry(
    entry_id: int,
    entry: EntryUpdate,
    user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    db_entry = db.query(Entry).get(entry_id)
    if not db_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )

    if user.role != "admin" and db_entry.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this entry",
        )

    db_entry.date = entry.date
    db_entry.time = entry.time
    db_entry.text = entry.text

    db.commit()
    return {"message": "Entry updated successfully"}


# API to delete the entries completely
@app.delete("/api/entries/{entry_id}")
async def delete_entry(
    entry_id: int,
    user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    db_entry = db.query(Entry).get(entry_id)
    if not db_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )

    if user.role != "admin" and db_entry.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this entry",
        )

    db.delete(db_entry)
    db.commit()
    return {"message": "Entry deleted successfully"}

# Driver code of the program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)