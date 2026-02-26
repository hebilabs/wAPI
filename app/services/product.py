from app.core.database import get_db


def list_products():
    conn = get_db()
    return conn.execute("SELECT * FROM products").fetchall()

def get_product(product_id: int):
    conn = get_db()
    return conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()