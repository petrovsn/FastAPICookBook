from fastapi import APIRouter, FastAPI


router_mod1 = APIRouter(prefix="/module1", tags=["module1"])


@router_mod1.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


@router_mod1.get("/ping", tags=["module1"])
async def ping():
    return {"message": "pong"}


@router_mod1.get("/raise_exception")
async def raise_exception():
    raise Exception("Some unawaitable exception")
    return {"message": "pong"}