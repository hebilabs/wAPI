from fastapi import APIRouter
from app.schemas.cart import CartCreate
from app.services.cart import add_to_cart

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add(cart: CartCreate):
    add_to_cart(cart)
    return {"message": "Added to cart"}