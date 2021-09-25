from typing import List, Optional
from sqlmodel import Field, Relationship,SQLModel
from pydantic import validator

class PortfolioBase(SQLModel):    
    name: str
    user_id: int
    
class PortfolioCreate(PortfolioBase): 
    pass

class PortfolioRead(PortfolioBase): 
    id: int

class PortfolioUpdate(PortfolioBase): 
    pass

class PortfolioDelete():
    id : int

class Portfolio(PortfolioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
class PortfolioInstruments(SQLModel, table=True):
    portfolio_id: int 
    instrument_id: int 