from fastapi import FastAPI
from calories import calories_routes
from fastapi_jwt_auth import AuthJWT
from schema import Settings
from auth import auth_routes





app = FastAPI()

#load jwt secret key
@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(calories_routes)
app.include_router(auth_routes)
