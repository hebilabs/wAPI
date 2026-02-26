from fastapi import APIRouter, Form, HTTPException
from fastapi.params import Depends
from app.core.security import get_current_user
from app.schemas.auth import LoginSchema
from app.services.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(payload: LoginSchema):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user["id"],
        "email": user["email"],
        "is_admin": user["is_admin"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.get("/me")
def get_profile(current_user=Depends(get_current_user)):
    print(f"Current user: {current_user}")
    return current_user