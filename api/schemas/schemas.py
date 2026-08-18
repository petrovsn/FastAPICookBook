from pydantic import BaseModel, model_validator, ConfigDict
from core.entities import Post

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class UserWithPostsOut(UserOut):
    model_config = ConfigDict(from_attributes=True)
    posts: list[Post]
    