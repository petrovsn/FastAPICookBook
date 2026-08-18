from fastapi import APIRouter, FastAPI, Depends, Body
from core.entities import AuthData
from api.schemas.schemas import UserOut, UserWithPostsOut
from core.use_cases import GetUsers, GetUser, InitiateDb
from db.repo import DatabaseUnitOfWork

router_mod2 = APIRouter(prefix="/module2", tags=["module2"])

async def get_uow_db():
    async with DatabaseUnitOfWork() as repo:
        yield repo

@router_mod2.post("/auth")
async def auth(auth_data: AuthData = Body(None)):
    if auth_data.user == "user" and auth_data.password == "12345":
        return {"auth_success":True}
    return {"auth_success":False}


@router_mod2.get("/initiate")
async def initiate_db(db_repo = Depends(get_uow_db)):
    result = await InitiateDb(db_repo).execute()
    return result

@router_mod2.get("/users")
async def get_users(db_repo = Depends(get_uow_db)) -> list[UserOut]:
    result = await GetUsers(db_repo).execute()
    return result

@router_mod2.post("/users/{id}")
async def get_user_with_post(id: int, db_repo = Depends(get_uow_db))  -> UserWithPostsOut:
    result = await GetUser(db_repo).execute(id)
    return result