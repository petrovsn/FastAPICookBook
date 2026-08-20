from fastapi import APIRouter, Depends, Header
from api.assembler.repo import get_uow_db
from core.use_cases import CreatePost, CreatePosts, GetPosts
from api.schemas.schemas import MoneyTransferRequest
router_mod4 = APIRouter(prefix="/module4", tags=["module4"])


@router_mod4.post("/transfer_money")
async def post_login(transfer_request: MoneyTransferRequest, db_repo = Depends(get_uow_db)):
    result = await TransferMoneyCase(db_repo).execute(transfer_request.from_user_id, 
                                                    transfer_request.to_user_id, 
                                                    transfer_request.amount)

    return result


@router_mod4.post("/create_posts/{user_id}")
async def post_alotof_posts(user_id: int, post_count: int, db_repo = Depends(get_uow_db)):
    result = await CreatePosts(db_repo).execute(user_id, post_count)
    return result


@router_mod4.post("/create_post/{user_id}")
async def post_post(user_id: int, post_text: str, db_repo = Depends(get_uow_db)):
    result = await CreatePost(db_repo).execute(user_id, post_text)
    return result

@router_mod4.get("/posts/paged_offset")
async def get_post_paged(
        offset: int = Header(0),
        limit: int = Header(10),
        db_repo = Depends(get_uow_db)):
    result = await GetPosts(db_repo).execute(offset, limit)
    return result

@router_mod4.get("/posts/paged_cursor")
async def get_post_paged_cursor(
        offset: int = Header(0),
        limit: int = Header(10),
        db_repo = Depends(get_uow_db)):
    result = await GetPosts(db_repo).execute(offset, limit, mode = "cursor")
    return result