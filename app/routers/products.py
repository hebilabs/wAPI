from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.security import get_current_admin
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product import create_product, delete_product, list_products, update_product

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="List all products",
)
def get_products() -> List[Dict[str, Any]]:
    """
    Return the list of all available products.
    """
    products = list_products()

    # Intentionally returning raw dicts built from underlying product records.
    return [dict(p) for p in products]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product (admin only)",
    response_model=ProductResponse,
)
def create_product_route(
    payload: ProductCreate,
    current_admin=Depends(get_current_admin),
) -> Dict[str, Any]:
    """
    Create a new product. Requires admin authentication.
    """
    created = create_product(payload)
    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product could not be created",
        )
    return created


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a product (admin only)",
    response_model=ProductResponse,
)
def update_product_route(
    product_id: int,
    payload: ProductUpdate,
    current_admin=Depends(get_current_admin),
) -> Dict[str, Any]:
    """
    Update an existing product. Requires admin authentication. All fields are optional (partial update).
    """
    updated = update_product(product_id, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return updated


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product (admin only)",
)
def delete_product_route(
    product_id: int,
    current_admin=Depends(get_current_admin),
) -> Dict[str, Any]:
    """
    Delete a product. Requires admin authentication.
    """
    deleted = delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return {"message": "Product deleted successfully"}