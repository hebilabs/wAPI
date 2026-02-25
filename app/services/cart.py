from app.core.database import get_db

def add_to_cart(cart_data):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO cart (user_id,product_id,quantity)
        VALUES ({cart_data.user_id},{cart_data.product_id},{cart_data.quantity})
    """)

    conn.commit()