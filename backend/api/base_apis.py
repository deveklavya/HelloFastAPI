from fastapi import APIRouter, Depends

from backend.api.v1 import users, secure

from backend.features.users.auth.auth_bearer import JWTBearer
from backend.db.database import get_session

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"],dependencies=[Depends(get_session)])

api_router.include_router(secure.router, tags=["secure"],dependencies=[Depends(JWTBearer())],responses={404: {"description": "Not found"}})

