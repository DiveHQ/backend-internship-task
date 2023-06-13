from fastapi import FastAPI
from src.routes.auth import auth_router
from src.routes.calories import calorie_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Calories Input API"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(calorie_router, prefix="/api/v1")

