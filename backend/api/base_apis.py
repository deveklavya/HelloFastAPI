from fastapi import APIRouter

from backend.api.v1 import heroes, teams, users


api_router = APIRouter()

api_router.include_router(heroes.router, tags=["heroes"])
api_router.include_router(teams.router, tags=["teams"])
api_router.include_router(users.router, tags=["users"])
