from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from backend.features.users.user_models import Token
from backend.features.users.user_service import UserService
from backend.db.database import get_session
from backend.api.dependencies import get_token

router = APIRouter()


@router.get("/secure/me/items/")
async def read_own_items(session: Session = Depends(get_session), token: str = Depends(get_token)):       
    current_user = await UserService(session, token).get_current_active_user()
    return [{"item_id": "Foo", "owner": current_user.username}]
