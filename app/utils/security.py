from jose import jwt
from app.core.config import get_settings

settings = get_settings()

def decode_token(token: str):
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        options={"verify_signature": False}  #not verifying signature, just decoding the payload
    )
    return payload