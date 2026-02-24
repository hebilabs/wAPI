from fastapi import APIRouter, Form, HTTPException
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()

    # sqli
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = cursor.execute(query).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return dict(user)