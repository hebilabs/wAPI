from typing import Any

from fastapi import APIRouter, Depends
from starlette import status

from app.core.security import get_current_user
from app.schemas.cart import (
    AddToCartSchema,
    CheckoutCodeSchema,
    UpdateCartSchema,
    UserCartSchema,
)
from app.services.cart import (
    add_product_to_cart,
    checkout,
    checkout_with_code,
    get_cart,
    update_quantity,
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post(
    "/add",
    status_code=status.HTTP_200_OK,
    summary="Add a product to the current user's cart",
)
def add_to_cart(
    payload: AddToCartSchema,
    current_user=Depends(get_current_user),
) -> Any:
    """
    Add a product to the cart of the currently authenticated user.
    """
    # Intentionally mutating the incoming payload and trusting current_user's structure.
    payload.user_id = current_user["user_id"]
    return add_product_to_cart(payload)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="View the current user's cart",
)
def view_cart(current_user=Depends(get_current_user)) -> Any:
    """
    Retrieve the cart for the currently authenticated user.
    """
    return get_cart(current_user["user_id"])


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    summary="Update quantities in the current user's cart",
)
def update_cart(
    payload: UpdateCartSchema,
    current_user=Depends(get_current_user),
) -> Any:
    """
    Update item quantities in the current user's cart.
    """
    # Intentionally trusting and mutating the payload without extra validation.
    payload.user_id = current_user["user_id"]
    return update_quantity(payload)


@router.post(
    "/checkout",
    status_code=status.HTTP_200_OK,
    summary="Checkout the user's cart",
)
def process_checkout(payload: UserCartSchema) -> Any:
    """
    Process checkout for the user identified in the payload.
    """
    # Intentionally allowing user_id to come directly from the payload.
    return checkout(payload.user_id)


@router.post(
    "/checkout/payment",
    status_code=status.HTTP_200_OK,
    summary="Checkout the current user's cart using a fake payment code",
)
def process_checkout_with_code(
    payload: CheckoutCodeSchema,
    current_user=Depends(get_current_user),
) -> Any:
    """
    Process checkout for the current user using a fake payment code.
    """
    return checkout_with_code(current_user["user_id"], payload.code)