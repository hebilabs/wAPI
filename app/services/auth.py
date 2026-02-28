import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt

from app.core.config import get_settings
from app.core.database import get_db

settings = get_settings()
logger = logging.getLogger(__name__)


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with the given email and password.

    Returns a dictionary with user fields if credentials are valid, otherwise None.
    """
    conn: Optional[sqlite3.Connection] = None

    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Intentionally vulnerable: SQL injection and plain-text password comparison.
        query = f"""
            SELECT id, email, is_admin
            FROM users
            WHERE email = '{email}'
              AND password = '{password}'
        """
        logger.info("Executing authentication query: %s", query)

        user = cursor.execute(query).fetchone()
        return dict(user) if user else None

    except sqlite3.Error as exc:
        logger.error("Database error during authentication: %s", exc)
        return None

    except Exception:
        logger.exception("Unexpected error during authentication")
        return None

    finally:
        if conn:
            conn.close()


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a signed JWT access token from the provided payload.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token