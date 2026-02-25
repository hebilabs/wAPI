from fastapi import APIRouter
from app.services.product import list_products

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_products():
    products = list_products()
    return [dict(p) for p in products]