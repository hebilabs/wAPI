from fastapi import APIRouter, Header, HTTPException
from app.utils.security import decode_token
from app.core.config import get_settings

router = APIRouter(prefix="/admin", tags=["Admin"])
settings = get_settings()

@router.get("/panel")
def admin_panel(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    #trusting the token payload without verifying the signature, just checking if is_admin is true so this on purpose ok?
    if payload.get("is_admin") == True:
        return {"flag": settings.FLAG}

    raise HTTPException(status_code=403, detail="Not admin")