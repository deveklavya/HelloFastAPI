from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select,  or_

from.user_models import Token,TokenData,UserRead,UserInDB, UserCreate
from .auth.auth_handler import AuthHandler


class UserService:
    def __init__(self, db_session):                   
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")        
        self.db = db_session

    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self,password):
        return self.pwd_context.hash(password)

    def create_user(self, user:UserCreate):
        user.disabled = False
        
        usr = UserInDB(full_name= user.full_name, email= user.email, 
                        username= user.username, hashed_password=self.get_password_hash(user.password), disabled=False)        
        
        self.db.add(usr)
        self.db.commit()
        self.db.refresh(usr)
        return usr

    def get_user(self, username: str):        
        statement = select(UserInDB).where(UserInDB.username == username)    
        return self.db.exec(statement).first()
        


    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(self):
        auth_handler = AuthHandler()
        try:            
            payload = auth_handler.decode_access_token() 
            username: str = payload.get("sub")
            if username is None:
                raise auth_handler.credentials_exception
            token_data = TokenData(username=username)
        except:
            raise auth_handler.credentials_exception

        user = self.get_user(username=token_data.username)       
        if user is None:
            raise auth_handler.credentials_exception
        return UserRead(**user.dict())


    async def get_current_active_user(self):
        current_user =  await self.get_current_user()        
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user