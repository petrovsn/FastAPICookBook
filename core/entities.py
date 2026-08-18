from pydantic import BaseModel, model_validator


class AuthData(BaseModel):
    user: str = "user"
    password: str = "12345"
    password_dup: str = "12345"

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.password_dup:
            raise ValueError("PASSWORD_MISMATCH")

        return self