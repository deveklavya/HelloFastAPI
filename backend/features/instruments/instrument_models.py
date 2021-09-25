from typing import List, Optional
from sqlmodel import Field, Relationship,SQLModel
from pydantic import validator

class InstrumentBase(SQLModel):    
    name: str
    exchange: str
    ticker: str
    asset_class: str
    
class InstrumentCreate(InstrumentBase): 
    pass

class InstrumentRead(InstrumentBase): 
    id: int

class InstrumentUpdate(InstrumentBase): 
    pass

class InstrumentDelete():
    id : int

class Instrument(InstrumentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
