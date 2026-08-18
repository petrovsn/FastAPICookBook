from fastapi import APIRouter, FastAPI, Depends, Body
from core.entities import AuthData

router_mod2 = APIRouter(prefix="/module2", tags=["module2"])


@router_mod2.post("/auth")
async def auth(auth_data: AuthData = Body(None)):
    if auth_data.user == "user":
        if auth_data.password == auth_data.password_dup == "12345":
            return {"auth_success":True}
    return {"auth_success":False}


