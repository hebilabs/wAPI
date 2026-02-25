from fastapi import APIRouter
from app.schemas.cart import AddToCartSchema
from app.services.cart import add_product_to_cart

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(payload: AddToCartSchema):
    return add_product_to_cart(payload)
