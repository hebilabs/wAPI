from typing import Any, Dict, List

from fastapi import APIRouter
from starlette import status

from app.services.product import list_products

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