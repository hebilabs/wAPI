from typing import Any

from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.cart import AddToCartSchema, UpdateCartSchema, UserCartSchema
from app.services.cart import add_product_to_cart, checkout, get_cart, update_quantity

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(payload: AddToCartSchema, current_user=Depends(get_current_user)):
    payload.user_id = current_user["user_id"]
    return add_product_to_cart(payload)


@router.get("/")
def view_cart(current_user=Depends(get_current_user)):
    return get_cart(current_user["user_id"])


@router.put("/update")
def update_cart(
    payload: UpdateCartSchema,
    current_user=Depends(get_current_user)
):
    payload.user_id = current_user["user_id"]
    return update_quantity(payload)


@router.post("/checkout")
def process_checkout(payload: UserCartSchema):
    return checkout(payload.user_id)