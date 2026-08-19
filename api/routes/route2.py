from fastapi import APIRouter, FastAPI, Depends, Body
from core.entities import AuthData
from api.schemas.schemas import UserOut, UserWithPostsOut, UserPatch
from core.use_cases import GetUsers, GetUser, InitiateDb, CreateUser, UpdateUser
from api.assembler.repo import get_uow_db

router_mod2 = APIRouter(prefix="/module2", tags=["module2"])



@router_mod2.post("/auth")
async def auth(auth_data: AuthData = Body(None)):
    if auth_data.user == "user" and auth_data.password == "12345":
        return {"auth_success":True}
    return {"auth_success":False}


@router_mod2.post("/initiate")
async def initiate_db(db_repo = Depends(get_uow_db)):
    result = await InitiateDb(db_repo).execute()
    return result

@router_mod2.get("/users")
async def get_users(db_repo = Depends(get_uow_db)) -> list[UserOut]:
    result = await GetUsers(db_repo).execute()
    return result

@router_mod2.post("/users")
async def post_user(user_patch: UserPatch, db_repo = Depends(get_uow_db)) -> UserOut:
    result = await CreateUser(db_repo).execute(user_patch.model_dump(exclude_unset=True))
    return result

@router_mod2.get("/users/{id}")
async def get_user_with_post(id: int, db_repo = Depends(get_uow_db))  -> UserWithPostsOut:
    result = await GetUser(db_repo).execute(id)
    return result

@router_mod2.patch("/users/{id}")
async def put_change_user(id: int, user_patch: UserPatch, db_repo = Depends(get_uow_db))  -> UserOut:
    result = await UpdateUser(db_repo).execute(id, user_patch.model_dump(exclude_unset=True))
    return result