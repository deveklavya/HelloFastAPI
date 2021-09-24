from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from.user_models import Token,TokenData,UserRead,UserInDB, UserCreate


class UserService:
    def __init__(self,db_session):    
        # to get a string like this run:
        # openssl rand -hex 32
        self.SECRET_KEY = "42d2d8785d813173c4bbeeb378318240db313ce789eb376c67c9f10bf6f569ca"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.db = db_session

    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self,password):
        return self.pwd_context.hash(password)

    def create_user(self, user:UserCreate):
        user.disabled = False
        
        usr = UserInDB(full_name= user.full_name, email= user.email, 
                        username= user.username, hashed_password=self.get_password_hash(user.password), diabled=False)        
        
        self.session.add(usr)
        self.session.commit()
        self.session.refresh(usr)
        return usr

    def get_user(self,db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)


    def authenticate_user(self,fake_db, username: str, password: str):
        user = self.get_user(fake_db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user


    def create_access_token(self,data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    async def get_current_user(self):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(self,self.oauth2_scheme, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


    async def get_current_active_user(current_user: UserRead = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user