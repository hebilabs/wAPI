import logging
import sqlite3
from typing import Any, List, Optional

from app.core.database import get_db

logger = logging.getLogger(__name__)


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