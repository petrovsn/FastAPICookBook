from fastapi import APIRouter, Depends
from api.assembler.repo import get_uow_db
from core.use_cases import TransferMoneyCase
from api.schemas.schemas import MoneyTransferRequest
router_mod4 = APIRouter(prefix="/module4", tags=["module4"])


@router_mod4.post("/transfer_money")
async def post_login(transfer_request: MoneyTransferRequest, db_repo = Depends(get_uow_db)):
    result = await TransferMoneyCase(db_repo).execute(transfer_request.from_user_id, 
                                                    transfer_request.to_user_id, 
                                                    transfer_request.amount)

    return result