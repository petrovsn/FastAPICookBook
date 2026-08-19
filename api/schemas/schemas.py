from pydantic import BaseModel, model_validator, ConfigDict
from core.entities import Post

class UserOut(BaseModel):
    id: int
    name: str
    email: str | None

class UserWithPostsOut(UserOut):
    posts: list[Post]

class UserPatch(BaseModel):
    email: str | None
    name: str | None

    @model_validator(mode="after")
    def check_passwords(self):
        if (self.email == self.name == None):
            raise ValueError("no no-None data")

        return self


