from fastapi import APIRouter, Header
from app.core.config import get_settings

router = APIRouter(prefix="/admin", tags=["Admin"])

settings = get_settings()

@router.get("/debug")
def debug(x_admin: str = Header(None)):
    if x_admin == settings.SECRET_KEY:
        return {"flag": settings.FLAG}
    return {"error": "Unauthorized"}