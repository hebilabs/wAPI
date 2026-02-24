from fastapi import APIRouter
from app.core.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])
#data ex
@router.get("/")
def list_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    return [dict(p) for p in products]