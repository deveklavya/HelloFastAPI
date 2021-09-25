from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select,  or_

from features.instruments.instrument_models import Instrument, InstrumentCreate, InstrumentUpdate
from features.portfolio.portfolio_models import PortfolioInstruments


class InstrumentService:
    def __init__(self, db_session):                   
        self.db =  db_session
    
    def create_instrument(self, instrument:InstrumentCreate):           
        db_instr = Instrument.from_orm(instrument)
        self.db.add(db_instr)
        self.db.commit()
        self.db.refresh(db_instr)
        return db_instr

    def read_instrument(self, instrument_id: int):           
        instrument = self.db.get(Instrument, instrument_id)
        if not instrument:
            raise HTTPException(status_code=404, detail="Instrument not found")
        return instrument

    def update_instrument(self, instrument:InstrumentUpdate, instrument_id: int):           
        db_instr = self.db .get(Instrument, instrument_id)
        if not db_instr:
            raise HTTPException(status_code=404, detail="Instrument not found")
        
        instrument_data = instrument.dict(exclude_unset=True)
        for key, value in instrument_data.items():
            setattr(db_instr, key, value)
        self.db.add(db_instr)
        self.db.commit()
        self.db.refresh(db_instr)
        return db_instr
    
    def delete_instrument(self, instrument_id: int):     
        self.delete_instruments_from_portfolio(instrument_id)
        db_instr = self.db.get(Instrument, instrument_id)
        if not db_instr:
            raise HTTPException(status_code=404, detail="Instrument not found")
        self.db.delete(db_instr)
        self.db.commit()
        return True

    def delete_instruments_from_portfolio(self, instrument_id: int):
        statement = select(PortfolioInstruments).where(PortfolioInstruments.instrument_id == instrument_id)
        results = self.db.exec(statement)
        all_ids = results.all()       
        if not all_ids:
            return True
        self.db.delete(all_ids)
        self.db.commit()
        return True

