from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select,  or_


from backend.features.portfolio.portfolio_models import Portfolio_Instruments, PortfolioCreate, PortfolioUpdate, Portfolio


class PortfolioService:
    def __init__(self, db_session):                   
        self.db =  db_session
    
    def create_portfolio(self, portfolio:PortfolioCreate):           
        db_instr = Portfolio.from_orm(portfolio)
        self.db.add(db_instr)
        self.db.commit()
        self.db.refresh(db_instr)
        return db_instr

    def read_portfolio(self, portfolio_id: int):           
        portfolio = self.db.get(Portfolio, portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return portfolio

    def update_portfolio(self, portfolio:PortfolioUpdate, portfolio_id: int):           
        db_instr = self.db .get(Portfolio, portfolio_id)
        if not db_instr:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_data = portfolio.dict(exclude_unset=True)
        for key, value in portfolio_data.items():
            setattr(db_instr, key, value)
        self.db.add(db_instr)
        self.db.commit()
        self.db.refresh(db_instr)
        return db_instr
    
    def delete_portfolio(self, portfolio_id: int):     
        self.delete_portfolio_references(portfolio_id)
        db_instr = self.db.get(Portfolio, portfolio_id)
        if not db_instr:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        self.db.delete(db_instr)
        self.db.commit()
        return True

    def delete_portfolio_references(self, portfolio_id: int):
        statement = select(Portfolio_Instruments).where(Portfolio_Instruments.portfolio_id == portfolio_id)
        results = self.db.exec(statement)
        all_ids = results.all()       
        if not all_ids:
            return True
        self.db.delete(all_ids)
        self.db.commit()
        return True

    def get_all_portfolios(self, user_id: int, offset: int, limit: int):
        statement = select(Portfolio).where(Portfolio.user_id == user_id).offset(offset).limit(limit)
        return self.db.exec(statement).all()
    
    def add_instrument_to_portfolio(self, portfolio_id:int, insrument_id: int):
        port = Portfolio_Instruments(portfolio_id = portfolio_id, instrument_id= insrument_id)
        db_instr = Portfolio_Instruments.from_orm(port)
        self.db.add(db_instr)
        self.db.commit()
        self.db.refresh(db_instr)
        return db_instr
    
    def get_instrument_and_portfolio(self, portfolio_id:int):
        statement = select(Portfolio_Instruments).where(Portfolio_Instruments.portfolio_id == portfolio_id)
        results = self.db.exec(statement)              
        if not results:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        return results.all() 
    
     
    def delete_portfolio_instrument(self, portfolio_instrument_id: int):             
        db_instr = self.db.get(Portfolio_Instruments, portfolio_instrument_id)
        if not db_instr:
            raise HTTPException(status_code=404, detail="Portfolio Instrument not found")
        self.db.delete(db_instr)
        self.db.commit()
        return True