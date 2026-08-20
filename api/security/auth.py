import jwt
from datetime import timezone, datetime, timedelta
from fastapi import Header, Depends
from api.assembler.repo import get_uow_db
from core.use_cases import GetUserByName

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


def get_token(user_name):
    payload = {
            "sub": user_name,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        }
    
    token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
    return token


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload["sub"]

    except jwt.PyJWTError:
        return None


async def get_user_dto_from_token(jwt_token: str = Header(...), db_repo = Depends(get_uow_db),)-> dict:
    username = verify_token(jwt_token)
    use_case = GetUserByName(db_repo)
    user_dto = await use_case.execute(username)
    if user_dto is None:
        raise Exception("no such user")
    return user_dto



from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/module3/login"
)

async def extract_token(
    token: str = Depends(oauth2_scheme),
):
    return token

async def get_user_dto_from_auth_schema(jwt_token = Depends(extract_token), db_repo = Depends(get_uow_db),)-> dict:
    username = verify_token(jwt_token)
    use_case = GetUserByName(db_repo)
    user_dto = await use_case.execute(username)
    return user_dto