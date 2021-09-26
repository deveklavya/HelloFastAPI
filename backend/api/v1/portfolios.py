from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional

from backend.db.database import get_session
from backend.features.portfolio.portfolio_models import PortfolioRead, PortfolioCreate, PortfolioUpdate, Portfolio_Instruments
from backend.features.portfolio.portfolio_service import PortfolioService

router = APIRouter()


@router.post("/create", response_model=PortfolioRead)
async def create_portfolio(*,portfolio: PortfolioCreate, session: Session = Depends(get_session)):
    return PortfolioService(session).create_portfolio(portfolio)

@router.get("/list/{user_id}", response_model=List[PortfolioRead])
def read_portfolios(*,
    user_id: int,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)):
    
    return PortfolioService(session).get_all_portfolios(user_id,offset, limit)


@router.get("/get/{portfolio_id}", response_model=PortfolioRead)
def read_portfolio(*,
    portfolio_id: int,
    session: Session = Depends(get_session) ):    
    return PortfolioService(session).read_portfolio(portfolio_id)

@router.patch("/update/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(
    *, session: Session = Depends(get_session), portfolio_id: int, portfolio: PortfolioUpdate):
    return PortfolioService(session).update_portfolio(portfolio, portfolio_id)

@router.delete("/delete/{portfolio_id}")
def delete_portfolio(*, session: Session = Depends(get_session), portfolio_id: int):
    return PortfolioService(session).delete_portfolio(portfolio_id)

@router.post("/add-instrument", response_model=Portfolio_Instruments)
async def add_instrument_portfolio(*,portfolio_id: int, instrument_id: int, session: Session = Depends(get_session)):
    port = PortfolioService(session).add_instrument_to_portfolio(portfolio_id,instrument_id)
    return port

@router.get("/get-instruments/{portfolio_id}", response_model=List[Portfolio_Instruments])
def read_portfolio(*,
    portfolio_id: int,
    session: Session = Depends(get_session) ):    
    ports = PortfolioService(session).get_instrument_and_portfolio(portfolio_id)
    return ports

@router.delete("/delete-instruments/{portfolio_id}")
def delete_portfolio(*, session: Session = Depends(get_session), portfolio_instrument_id: int):
    return PortfolioService(session).delete_portfolio_instrument(portfolio_instrument_id)
