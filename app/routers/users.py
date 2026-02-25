from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.services.user import get_user_by_id, create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    return dict(user)


@router.post("/")
def create(user: UserCreate):
    create_user(user)
    return {"message": "User created"}