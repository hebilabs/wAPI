from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.core.security import get_current_user
from app.schemas.auth import LoginSchema
from app.services.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and obtain access token",
)
def login(payload: LoginSchema) -> Dict[str, Any]:
    """
    Authenticate a user with email and password and return an access token.
    """
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Intentionally including email and is_admin directly in the token payload.
    token = create_access_token(
        {
            "user_id": user["id"],
            "email": user["email"],
            "is_admin": user["is_admin"],
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
)
def get_profile(current_user=Depends(get_current_user)) -> Any:
    """
    Return the profile of the current authenticated user.
    """
    return current_user