from fastapi import APIRouter, Depends

from backend.api.v1 import users, secure, portfolios, instruments

from backend.features.users.auth.auth_bearer import JWTBearer
from backend.db.database import get_session

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"],dependencies=[Depends(get_session)])
api_router.include_router(secure.router, tags=["secure"],dependencies=[Depends(JWTBearer())],responses={404: {"description": "Not found"}})

api_router.include_router(portfolios.router, prefix="/portfolio", tags=["portfolio"], dependencies=[Depends(get_session)])
api_router.include_router(instruments.router, prefix="/instruments", tags=["instrument"], dependencies=[Depends(get_session)])
