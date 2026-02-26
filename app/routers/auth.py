from fastapi import APIRouter, Form, HTTPException
from app.schemas.auth import LoginSchema
from app.services.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(payload: LoginSchema):
    print(f"Received login : email={payload.email}, password={payload.password}")
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