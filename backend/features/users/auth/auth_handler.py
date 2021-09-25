from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer


import logging

class AuthHandler:
    def __init__(self):  
        # to get a string like this run:
        # openssl rand -hex 32
        self.SECRET_KEY = "42d2d8785d813173c4bbeeb378318240db313ce789eb376c67c9f10bf6f569ca"
        self.ALGORITHM = "HS256"   
        self.credentials_exception = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentials Bad token",
                                        headers={"WWW-Authenticate": "Bearer"},
                                    )     
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
        self.ACCESS_TOKEN_EXPIRE_MINUTES= 50


    def create_access_token(self,data: dict, expires_delta: Optional[timedelta] = None):
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=15)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
            return encoded_jwt

    def token_response(token: str):
        return {
            "access_token": token
        }

    def decode_access_token(self, token: Optional[str] = None):             
        try:
            logger = logging.getLogger(__name__)
            logger.info("Token Value is : " + token)
            return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except JWTError:
            raise self.credentials_exception 
