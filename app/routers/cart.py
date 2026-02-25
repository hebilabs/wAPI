from fastapi import APIRouter
from app.schemas.cart import AddToCartSchema, UpdateCartSchema, UserCartSchema
from app.services.cart import add_product_to_cart, checkout, get_cart, update_quantity

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(payload: AddToCartSchema):
    return add_product_to_cart(payload)


@router.get("/{user_id}")
def view_cart(user_id: int):
    return get_cart(user_id)


@router.put("/update")
def update_cart(payload: UpdateCartSchema):
    return update_quantity(payload)


@router.post("/checkout")
def process_checkout(payload: UserCartSchema):
    return checkout(payload.user_id)