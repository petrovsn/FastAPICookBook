from pydantic import BaseModel, model_validator, ConfigDict
from core.entities import Post

class UserOut(BaseModel):
    id: int
    name: str
    email: str | None

class UserWithPostsOut(UserOut):
    posts: list[Post]

class UserPatch(BaseModel):
    email: str | None = None
    name: str | None = None

    @model_validator(mode="after")
    def check_passwords(self):
        if (self.email == self.name == None):
            raise ValueError("no no-None data")

        return self


from uuid import UUID
from pydantic import BaseModel
from pydantic_core import core_schema

class UUID7:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type,
        handler,
    ):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.uuid_schema(
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda value: value.hex
                )
            ),
        )

    @classmethod
    def validate(cls, value: UUID) -> UUID:
        if value.version != 7:
            raise ValueError("UUID must be version 7")

        return value