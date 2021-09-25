from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional

from backend.db.database import get_session
from backend.features.instruments.instrument_models import InstrumentRead, InstrumentCreate, InstrumentUpdate
from backend.features.instruments.instrument_service import InstrumentService

router = APIRouter()


router.post("/create", response_model=InstrumentRead)
async def create_hero(*,instrument: InstrumentCreate, session: Session = Depends(get_session)):
    return InstrumentService(session).create_instrument(instrument)

router.get("/list/{user_id}", response_model=List[InstrumentRead])
def read_heroes(*,
    user_id: int,
    session: Session = Depends(get_session),
    offset: int = Query(default=0),
    limit: int = Query(default=100, lte=100)):
    
    return InstrumentService(session).get_all_Instruments(user_id,offset, limit)


router.get("/get/{instrument_id}", response_model=InstrumentRead)
def read_Instruments(*,
    instrument_id: int,
    session: Session = Depends(get_session) ):    
    return InstrumentService(session).read_Instrument(instrument_id)

router.patch("/update/{instrument_id}", response_model=InstrumentRead)
def update_Instrument(
    *, session: Session = Depends(get_session), instrument_id: int, instrument: InstrumentUpdate):
    return InstrumentService(session).update_instrument(instrument, instrument_id)

router.delete("/delete/{instrument_id}")
def delete_Instrument(*, session: Session = Depends(get_session), instrument_id: int):
    return InstrumentService(session).delete_instrument(instrument_id)
    