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