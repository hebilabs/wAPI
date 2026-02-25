from app.core.database import get_db
from app.schemas.cart import AddToCartSchema


def add_product_to_cart(payload: AddToCartSchema):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, quantity FROM cart
        WHERE user_id = ? AND product_id = ?
    """, (payload.user_id, payload.product_id))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE cart
            SET quantity = quantity + 1
            WHERE id = ?
        """, (existing[0],))
    else:
        cursor.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, 1)
        """, (payload.user_id, payload.product_id))

    conn.commit()
    conn.close()

    return {"message": "Product added to cart"}
