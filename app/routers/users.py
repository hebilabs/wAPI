from typing import Any, Dict

from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from app.schemas.user import UserCreate, UserResponse
from app.services.user import get_user_by_id, create_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user by ID",
    response_model=UserResponse, 
)
def get_user(user_id: int) -> Dict[str, Any]:
    """
    Return a single user by its numeric identifier.
    """
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return dict(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_model=UserResponse,  
)
def create_user_route(user: UserCreate) -> Dict[str, Any]:
    """
    Create a new user using the provided payload.
    """
    created_user = create_user(user)

    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created or email already exists",
        )

    # Returning the full user including password, is_admin
    return created_user