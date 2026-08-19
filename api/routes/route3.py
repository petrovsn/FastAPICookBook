from fastapi import APIRouter, FastAPI, Depends, Body
from core.entities import AuthData
from api.schemas.schemas import UserOut, UserWithPostsOut, UserPatch
from core.use_cases import GetUsers, GetUser, InitiateDb, CreateUser, UpdateUser,GetUserByName
from db.repo import DatabaseUnitOfWork
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from api.assembler.repo import get_uow_db
from api.security.auth import get_token

router_mod3 = APIRouter(prefix="/module3", tags=["module3"])


@router_mod3.post("/login")
async def login(username: str, db_repo = Depends(get_uow_db)):
    user = await GetUserByName(db_repo).execute(username)
    if user is not None:
        token = get_token(user["name"])
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    raise Exception("no such user")