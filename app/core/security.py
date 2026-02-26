from http.client import HTTPException

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from app.core.config import get_settings

settings = get_settings()
security = HTTPBearer()

def decode_token(token: str):
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        options={"verify_signature": False}  #not verifying signature, just decoding the payload
    )
    return payload

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")