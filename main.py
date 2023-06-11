
from fastapi import FastAPI
from routes.auth import auth_router
from routes.calories import calorie_router
from routes.manager import manager_router
from routes.admin import admin_calorie_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Calories Input API"}

app.include_router(auth_router, prefix="/api/v1")
app.include_router(calorie_router, prefix="/api/v1")
app.include_router(manager_router, prefix="/api/v1")
app.include_router(admin_calorie_router, prefix="/api/v1")