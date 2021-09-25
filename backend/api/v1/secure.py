from fastapi import APIRouter, Depends, HTTPException, Query, status
from backend.features.users.user_models import Token

router = APIRouter()

@router.get("/secure", response_model=Token)
async def logout_access_token():    
    access_token = ""
    return {"access_token": access_token, "token_type": "bearer"}