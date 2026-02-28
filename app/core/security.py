from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from app.core.config import get_settings
from jose.exceptions import JWTError

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
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Require a valid Bearer token and that the token payload has is_admin truthy.
    Intentionally trusts the token payload (same as admin panel).
    """
    payload = decode_token(credentials.credentials)
    if not payload.get("is_admin"):
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return payload