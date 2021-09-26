from typing import List, Optional
from sqlmodel import Field, Relationship,SQLModel
from pydantic import validator
from datetime import datetime

class InstrumentDataBase(SQLModel):      
    ticker: str
    trade_date: datetime
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    avg_price:float
    vol:float
    
class InstrumentDataCreate(InstrumentDataBase): 
    pass

class InstrumentDataRead(InstrumentDataBase): 
    id: int

class InstrumentDataUpdate(InstrumentDataBase): 
    pass

class InstrumentDataDelete():
    id : int

class Instrument_Data_Daily(InstrumentDataBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



