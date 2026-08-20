from fastapi import APIRouter, FastAPI, Depends, Body, Header
from core.entities import AuthData
from api.schemas.schemas import UserOut, UserWithPostsOut, UserPatch
from core.use_cases import GetUsers, GetUser, InitiateDb, CreateUser, UpdateUser,GetUserByName
from db.repo import DatabaseUnitOfWork
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from api.assembler.repo import get_uow_db
from api.security.auth import get_token, verify_token,get_user_dto_from_token,get_user_dto_from_auth_schema

router_mod3 = APIRouter(prefix="/module3", tags=["module3"])


@router_mod3.post("/login")
async def post_login(username: str, db_repo = Depends(get_uow_db)):
    user = await GetUserByName(db_repo).execute(username)
    if user is not None:
        token = get_token(user["name"])
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    raise Exception("no such user")


@router_mod3.get("/verify_token")
async def get_token_verification(jwt_token: str = Header()):
    username = verify_token(jwt_token)
    if username is not None:
        return {
            "user_name": username,
            "token_is_active":True
        }
    return {
                "token_is_active":False
        }

@router_mod3.get("/verify_token2")
async def get_token_verification2(user_dto = Depends(get_user_dto_from_token)):
    if user_dto is not None:
        return {
            "user_name": user_dto["name"],
            "user_email": user_dto["email"],
            "token_is_active":True
        }
    return {
                "token_is_active":False
        }


from fastapi.security import OAuth2PasswordRequestForm
@router_mod3.post("/login3")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    username = form_data.username
    password = form_data.password

    # проверяем username/password
    # создаём JWT

    token = get_token(username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router_mod3.get("/verify_token3")
async def get_token_verification3(user_dto = Depends(get_user_dto_from_auth_schema)):
    if user_dto is not None:
        return {
            "user_name": user_dto["name"],
            "user_email": user_dto["email"],
            "token_is_active":True
        }
    return {
                "token_is_active":False
        }