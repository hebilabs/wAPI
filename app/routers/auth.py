from fastapi import APIRouter, Form, HTTPException
from app.services.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user["id"],
        "username": user["username"],
        "is_admin": user["is_admin"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }