from fastapi import APIRouter, Depends, HTTPException, status
from models import Session, engine, User, RevokedToken
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from schema import UserCreate, UserUpdate, UserSignin
from fastapi.encoders import jsonable_encoder



auth =  APIRouter(tags="Authentication")

session = Session(bind=engine)



#function to check if the jwt token has been revoked or not
async def is_token_revoked(jti: str):
   # Query the database for the token ID
    revoked_token = session.query(RevokedToken).filter_by(id=jti).first()
    return revoked_token is not None

#function to create token manager to use jwt token and confirm user login
async def token_manager(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti= Authorize.get_raw_jwt()["jti"]
        

        # Check if the token is revoked
        if await is_token_revoked(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        #get the current user
        current_user = Authorize.get_jwt_subject()
        return current_user
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    


@auth.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def new_user(user:UserCreate):

    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")
    new_user = User(email=user.email, password=generate_password_hash(user.password),
                    role= user.role)
    session.add(new_user)
    session.commit()
    return {"message":"New user created"}


@auth.post("/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(user:UserSignin, Authorize:AuthJWT=Depends()):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email does not exist")
    if not check_password_hash(existing_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect.")

    access_token = Authorize.create_access_token(subject=user.email)
    response =  {"access_token":access_token}
    return jsonable_encoder(response)
    

# #route to log out user
@auth.post("/sign_out", status_code=status.HTTP_200_OK)
def sign_out(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()["jti"]
        
        # Create a new instance of RevokedToken and save it in the database
        revoked_token = RevokedToken(id=jti)
        session.add(revoked_token)
        session.commit()
        
        
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")


