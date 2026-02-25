from fastapi import APIRouter, Form, HTTPException
from app.services.auth import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return dict(user)