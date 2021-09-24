from fastapi import APIRouter

from backend.api.v1 import heroes
from backend.api.v1 import teams

api_router = APIRouter()

api_router.include_router(heroes.router, tags=["heroes"])
api_router.include_router(teams.router, tags=["teams"])
