from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException
from app.schemas.user import UserCreate
from app.services.user import get_user_by_id, create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    return dict(user)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: UserCreate):
    created_user = create_user(user)

    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created or email already exists"
        )

    return {
        "message": "User created successfully",
        "data": created_user
    }
