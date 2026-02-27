import sqlite3
from asyncio.log import logger
from typing import Any, Dict, Optional

from app.core.database import get_db


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single user by its numeric identifier.

    Returns a dictionary representation of the user row if found, otherwise None.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row

        # Intentionally using string interpolation (SQL injection risk kept on purpose).
        query = f"SELECT * FROM users WHERE id = {user_id}"
        logger.info("Executing user lookup query: %s", query)

        row = conn.execute(query).fetchone()
        return dict(row) if row else None

    except sqlite3.IntegrityError as exc:
        logger.warning("Integrity error while getting user: %s", exc)
        return None

    except sqlite3.Error as exc:
        logger.error("Database error while getting user: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error while getting user")
        return None

    finally:
        if conn:
            conn.close()


def create_user(user_data: Any) -> Optional[Dict[str, Any]]:
    """
    Create a new user using the provided user_data object.

    Returns a dictionary with selected user fields if creation succeeds, otherwise None.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Intentionally vulnerable: interpolating email directly into SQL.
        check_query = f"SELECT id FROM users WHERE email = '{user_data.email}'"
        logger.info("Checking existing email with query: %s", check_query)

        existing_user = cursor.execute(check_query).fetchone()
        if existing_user:
            logger.warning("Attempt to register existing email: %s", user_data.email)
            return None

        # Intentionally vulnerable: plain-text password, mass assignment, SQL injection.
        insert_query = f"""
            INSERT INTO users (fullname, email, password, address, is_admin)
            VALUES (
                '{user_data.fullname}',
                '{user_data.email}',
                '{user_data.password}',
                '{user_data.address}',
                {int(user_data.is_admin)}
            )
        """
        logger.info("Executing insert query: %s", insert_query)

        cursor.execute(insert_query)
        conn.commit()
        user_id = cursor.lastrowid

        # Still using string interpolation, no parameterization.
        select_query = f"""
            SELECT id, fullname, email, password, address, is_admin
            FROM users
            WHERE id = {user_id}
        """
        logger.info("Fetching created user with query: %s", select_query)

        user = cursor.execute(select_query).fetchone()
        return dict(user) if user else None

    except sqlite3.IntegrityError as exc:
        logger.warning("Integrity error while creating user: %s", exc)
        return None

    except sqlite3.Error as exc:
        logger.error("Database error while creating user: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error while creating user")
        return None

    finally:
        if conn:
            conn.close()