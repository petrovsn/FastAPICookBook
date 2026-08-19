import jwt
from datetime import timezone, datetime, timedelta

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
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        if  expires_at > datetime.now(timezone.utc):
            return payload["sub"]
        raise jwt.PyJWTError("token is expired")
    
    except jwt.PyJWTError:
        return None