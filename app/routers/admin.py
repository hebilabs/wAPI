from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from starlette import status

from app.core.config import get_settings
from app.utils.security import decode_token

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

settings = get_settings()


@router.get(
    "/panel",
    status_code=status.HTTP_200_OK,
    summary="Access the admin panel",
)
def admin_panel(authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    """
    Return the admin panel flag for users marked as admin in the token payload.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    # Intentionally naive parsing: assumes 'Bearer <token>' and does not validate structure.
    parts = authorization.split(" ")
    if len(parts) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authorization header format",
        )

    token = parts[1]

    # Intentionally trusting the token payload without verifying the signature.
    payload = decode_token(token)

    if payload.get("is_admin") is True:
        return {"flag": settings.FLAG}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not admin",
    )