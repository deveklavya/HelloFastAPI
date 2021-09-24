from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel

class UserBase(SQLModel):    
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None    

class UserCreate(UserBase): 
    password: str


class UserRead(UserBase): 
    pass

class UserInDB(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None