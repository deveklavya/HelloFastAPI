from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from backend.db.database import get_session
from backend.features.users.user_models import Token, TokenData, UserRead, UserCreate
from backend.features.users.user_service import UserService


router = APIRouter()

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
    access_token_expires = timedelta(minutes=user_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=UserRead)
async def register_user(*, session: Session = Depends(get_session), user: UserCreate):
    
    # check for username and email they must be unique

    
    user_service = UserService(session)
    return user_service.create_user(user)


@router.get("/users/me/", response_model=UserRead)
async def read_users_me(session: Session = Depends(get_session)):   
    return UserService(session).get_current_active_user()


@router.get("/users/me/items/")
async def read_own_items(session: Session = Depends(get_session)):
    current_user = UserService(session).get_current_active_user()
    return [{"item_id": "Foo", "owner": current_user.username}]