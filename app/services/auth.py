from dbm import sqlite3
from typing import Dict, Optional

from app.core.database import get_db
from app.core.config import get_settings
from jose import jwt
from datetime import datetime, timedelta
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    conn = None
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # SQLi vuln intentionally
        query = f"""
            SELECT id, email, role
            FROM users
            WHERE email = '{email}'
            AND password = '{password}'
        """

        logger.info("Executing query: %s", query)
        user = cursor.execute(query).fetchone()

        if user:
            return dict(user)

        return None
    except sqlite3.Error as e:
        logger.error("Database error during authentication: %s", str(e))
        return None
    except Exception as e:
        logger.exception("Unexpected error during authentication")
        return None
    finally:
        if conn:
            conn.close()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token
