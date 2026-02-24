from fastapi import APIRouter
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

#bola
@router.get("/{user_id}")
def get_user(user_id: int):
    conn = get_db()
    user = conn.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    return dict(user)