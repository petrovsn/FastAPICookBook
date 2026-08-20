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