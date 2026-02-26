from app.core.database import get_db
from app.schemas.cart import AddToCartSchema, UpdateCartSchema


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
            INSERT INTO cart (user_id, product_id, image_url, quantity)
            VALUES (?, ?, ?, 1)
        """, (payload.user_id, payload.product_id, payload.image_url))

    conn.commit()
    conn.close()

    return {"message": "Product added to cart"}


def get_cart(user_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.name, p.price, c.quantity, p.image_url 
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))

    items = cursor.fetchall()
    conn.close()

    cart_items = []
    total = 0

    for item in items:
        product_total = item[2] * item[3]
        total += product_total

        cart_items.append({
            "product_id": item[0],
            "name": item[1],
            "price": item[2],
            "quantity": item[3],
            "image_url": item[4],
            "subtotal": product_total
        })

    return {
        "items": cart_items,
        "total": total
    }


def checkout(user_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))

    items = cursor.fetchall()

    total = sum(price * qty for price, qty in items)

    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    return {
        "message": "Checkout completed",
        "total_paid": total
    }


def update_quantity(payload: UpdateCartSchema):
    conn = get_db()
    cursor = conn.cursor()
    print(f"Update cart: ${payload}")

    if payload.quantity <= 0:
        cursor.execute("""
            DELETE FROM cart
            WHERE user_id = ? AND product_id = ?
        """, (payload.user_id, payload.product_id))
    else:
        cursor.execute("""
            UPDATE cart
            SET quantity = ?
            WHERE user_id = ? AND product_id = ?
        """, (payload.quantity, payload.user_id, payload.product_id))

    conn.commit()
    conn.close()

    return {"message": "Cart updated"}


def remove_item(payload):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE user_id = ? AND product_id = ?
    """, (payload.user_id, payload.product_id))

    conn.commit()
    conn.close()

    return {"message": "Item removed"}