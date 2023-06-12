from fastapi import FastAPI
from auth import auth
from fastapi_jwt_auth import AuthJWT
from schema import Settings




app = FastAPI()

#load jwt secret key
@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth)