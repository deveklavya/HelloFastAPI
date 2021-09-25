from fastapi import APIRouter, Depends

from backend.api.v1 import users, secure

from backend.features.users.auth.auth_bearer import JWTBearer

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])

api_router.include_router(secure.router, tags=["secure"],dependencies=[Depends(JWTBearer())],responses={404: {"description": "Not found"}})

