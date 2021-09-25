from typing import List, Optional
from sqlmodel import Field, Relationship,SQLModel
from pydantic import validator

class UserBase(SQLModel):    
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None    

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
    
    @validator('full_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

class UserCreate(UserBase): 
    password: str
    @validator('password')
    def passwords_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

class UserRead(UserBase): 
    pass

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None