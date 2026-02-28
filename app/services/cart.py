import logging
import sqlite3
from typing import Any, Dict, Optional

from app.core.database import get_db
from app.schemas.cart import AddToCartSchema, UpdateCartSchema

logger = logging.getLogger(__name__)


def add_product_to_cart(payload: AddToCartSchema) -> Dict[str, Any]:
    """
    Add a product to the user's cart, incrementing quantity if it already exists.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info(
            "Adding product to cart | user_id=%s product_id=%s",
            payload.user_id,
            payload.product_id,
        )

        cursor.execute(
            """
            SELECT id, quantity FROM cart
            WHERE user_id = ? AND product_id = ?
            """,
            (payload.user_id, payload.product_id),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE cart
                SET quantity = quantity + 1
                WHERE id = ?
                """,
                (existing[0],),
            )
        else:
            cursor.execute(
                """
                INSERT INTO cart (user_id, product_id, image_url, quantity)
                VALUES (?, ?, ?, 1)
                """,
                (payload.user_id, payload.product_id, payload.image_url),
            )

        conn.commit()
        return {"message": "Product added to cart"}

    except sqlite3.Error as exc:
        logger.error("Database error while adding to cart: %s", exc)
        return {"message": "Error adding product to cart"}

    except Exception:
        logger.exception("Unexpected error while adding to cart")
        return {"message": "Error adding product to cart"}

    finally:
        if conn:
            conn.close()


def get_cart(user_id: int) -> Dict[str, Any]:
    """
    Retrieve the cart for the given user identifier.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info("Fetching cart for user_id=%s", user_id)

        cursor.execute(
            """
            SELECT p.id, p.name, p.price, c.quantity, p.image_url
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            """,
            (user_id,),
        )

        items = cursor.fetchall()

        cart_items = []
        total = 0.0

        for product_id, name, price, quantity, image_url in items:
            product_total = price * quantity
            total += product_total

            cart_items.append(
                {
                    "product_id": product_id,
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                    "image_url": image_url,
                    "subtotal": product_total,
                }
            )

        return {
            "items": cart_items,
            "total": total,
        }

    except sqlite3.Error as exc:
        logger.error("Database error while getting cart: %s", exc)
        return {"items": [], "total": 0}

    except Exception:
        logger.exception("Unexpected error while getting cart")
        return {"items": [], "total": 0}

    finally:
        if conn:
            conn.close()


def checkout(user_id: int) -> Dict[str, Any]:
    """
    Perform a checkout for the given user, returning the total paid.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info("Checking out cart for user_id=%s", user_id)

        cursor.execute(
            """
            SELECT p.price, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            """,
            (user_id,),
        )
        items = cursor.fetchall()

        total = sum(price * qty for price, qty in items)

        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()

        return {
            "message": "Checkout completed",
            "total_paid": total,
        }

    except sqlite3.Error as exc:
        logger.error("Database error during checkout: %s", exc)
        return {"message": "Checkout failed", "total_paid": 0}

    except Exception:
        logger.exception("Unexpected error during checkout")
        return {"message": "Checkout failed", "total_paid": 0}

    finally:
        if conn:
            conn.close()


def update_quantity(payload: UpdateCartSchema) -> Dict[str, Any]:
    """
    Update or remove an item from the cart based on the requested quantity.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info(
            "Updating cart quantity | user_id=%s product_id=%s quantity=%s",
            payload.user_id,
            payload.product_id,
            payload.quantity,
        )

        if payload.quantity <= 0:
            cursor.execute(
                """
                DELETE FROM cart
                WHERE user_id = ? AND product_id = ?
                """,
                (payload.user_id, payload.product_id),
            )
        else:
            cursor.execute(
                """
                UPDATE cart
                SET quantity = ?
                WHERE user_id = ? AND product_id = ?
                """,
                (payload.quantity, payload.user_id, payload.product_id),
            )

        conn.commit()
        return {"message": "Cart updated"}

    except sqlite3.Error as exc:
        logger.error("Database error while updating cart: %s", exc)
        return {"message": "Error updating cart"}

    except Exception:
        logger.exception("Unexpected error while updating cart")
        return {"message": "Error updating cart"}

    finally:
        if conn:
            conn.close()


def remove_item(payload: Any) -> Dict[str, Any]:
    """
    Remove a specific item from the user's cart.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info(
            "Removing item from cart | user_id=%s product_id=%s",
            payload.user_id,
            payload.product_id,
        )

        cursor.execute(
            """
            DELETE FROM cart
            WHERE user_id = ? AND product_id = ?
            """,
            (payload.user_id, payload.product_id),
        )

        conn.commit()
        return {"message": "Item removed"}

    except sqlite3.Error as exc:
        logger.error("Database error while removing item: %s", exc)
        return {"message": "Error removing item"}

    except Exception:
        logger.exception("Unexpected error while removing item")
        return {"message": "Error removing item"}

    finally:
        if conn:
            conn.close()