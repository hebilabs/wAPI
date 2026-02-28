import logging
import sqlite3
from typing import Any, Dict, List, Optional

from app.core.database import get_db

logger = logging.getLogger(__name__)


def create_product(product_data: Any) -> Optional[Dict[str, Any]]:
    """
    Create a new product. Returns the created product as a dict if successful, otherwise None.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products (name, description, price, image_url, internal_cost)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                product_data.name,
                product_data.description,
                product_data.price,
                product_data.image_url,
                product_data.internal_cost,
            ),
        )
        conn.commit()
        product_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, name, description, price, image_url, internal_cost FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    except sqlite3.Error as exc:
        logger.error("Database error while creating product: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error while creating product")
        return None

    finally:
        if conn:
            conn.close()


def update_product(product_id: int, product_data: Any) -> Optional[Dict[str, Any]]:
    """
    Update an existing product by id. Returns the updated product as a dict if found, otherwise None.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            return None

        updates = []
        params = []
        if product_data.name is not None:
            updates.append("name = ?")
            params.append(product_data.name)
        if product_data.description is not None:
            updates.append("description = ?")
            params.append(product_data.description)
        if product_data.price is not None:
            updates.append("price = ?")
            params.append(product_data.price)
        if product_data.image_url is not None:
            updates.append("image_url = ?")
            params.append(product_data.image_url)
        if product_data.internal_cost is not None:
            updates.append("internal_cost = ?")
            params.append(product_data.internal_cost)

        if not updates:
            cursor.execute(
                "SELECT id, name, description, price, image_url, internal_cost FROM products WHERE id = ?",
                (product_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

        params.append(product_id)
        cursor.execute(
            f"UPDATE products SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        conn.commit()

        cursor.execute(
            "SELECT id, name, description, price, image_url, internal_cost FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    except sqlite3.Error as exc:
        logger.error("Database error while updating product: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error while updating product")
        return None

    finally:
        if conn:
            conn.close()


def delete_product(product_id: int) -> bool:
    """
    Delete a product by id. Returns True if a row was deleted, False otherwise.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        logger.info("Deleting product id=%s", product_id)

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as exc:
        logger.error("Database error while deleting product: %s", exc)
        return False

    except Exception:
        logger.exception("Unexpected error while deleting product")
        return False

    finally:
        if conn:
            conn.close()


def list_products() -> List[Any]:
    """
    Return all products from the database.

    The returned items are sqlite rows; routers convert them to dicts.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row

        query = "SELECT * FROM products"
        logger.info("Executing product list query: %s", query)

        return conn.execute(query).fetchall()

    except sqlite3.Error as exc:
        logger.error("Database error while listing products: %s", exc)
        return []

    except Exception:
        logger.exception("Unexpected error while listing products")
        return []

    finally:
        if conn:
            conn.close()


def get_product(product_id: int) -> Optional[Any]:
    """
    Retrieve a single product by its identifier.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row

        query = "SELECT * FROM products WHERE id = ?"
        logger.info("Executing product lookup query: %s | id=%s", query, product_id)

        return conn.execute(query, (product_id,)).fetchone()

    except sqlite3.Error as exc:
        logger.error("Database error while getting product: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error while getting product")
        return None

    finally:
        if conn:
            conn.close()