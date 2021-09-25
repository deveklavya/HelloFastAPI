from backend.features.users.auth.auth_handler import AuthHandler
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select,  or_
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from backend.db.database import get_session
from backend.features.users.user_models import Token, TokenData, UserRead, UserCreate,UserInDB
from backend.features.users.user_service import UserService
from backend.features.users import AuthHandler


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user_service = UserService(session)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    auth_handler = AuthHandler()
    access_token_expires = timedelta(minutes=auth_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout", response_model=Token)
async def logout_access_token():    
    access_token = ""
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
async def register_user(*, session: Session = Depends(get_session), user: UserCreate):    
    # check for username and email they must be unique
    statement = select(UserInDB).where(or_(UserInDB.username == user.username, UserInDB.email ==  user.email))    
    results = session.exec(statement).first()
    print(results)
    if results != None:
        raise HTTPException(status_code=404, detail="Duplicate username or email found ")        
    
    user_service = UserService(session,oauth2_scheme)
    return user_service.create_user(user)
    

@router.get("/users/me/", response_model=UserRead)
async def read_users_me(session: Session = Depends(get_session)):       
    user =  await UserService(session,oauth2_scheme).get_current_active_user()
    #print("Token", user.dict())
    return user


@router.get("/users/me/items/")
async def read_own_items(session: Session = Depends(get_session),oauth2_scheme: str = Depends(oauth2_scheme)):       
    current_user = await UserService(session,oauth2_scheme).get_current_active_user()
    return [{"item_id": "Foo", "owner": current_user.username}]
