from pydantic import BaseModel, model_validator, ConfigDict, field_validator
from core.entities import Post

class UserOut(BaseModel):
    id: int
    name: str
    email: str | None
    money: int

class UserWithPostsOut(UserOut):
    posts: list[Post]

class UserPatch(BaseModel):
    email: str | None = None
    name: str | None = None
    money: int | None = None

class MoneyTransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: int

    @field_validator("amount", mode="after")
    @classmethod
    def check_amount(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Transfer can't be negative")
        return value


class PaginationRequest(BaseModel):
    offset: int | None = None
    limit: int | None = None