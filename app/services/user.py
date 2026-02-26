from asyncio.log import logger
import sqlite3
from typing import Dict, Optional

from app.core.database import get_db

def get_user_by_id(user_id: int):
    conn = None
    try:
        conn = get_db()
        return conn.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    except sqlite3.IntegrityError as e:
        logger.warning("Integrity error while getting user: %s", str(e))
        return None

    except sqlite3.Error as e:
        logger.error("Database error while getting user: %s", str(e))
        return None

    except Exception:
        logger.exception("Unexpected error while getting user")
        return None
    finally:
        if conn:
            conn.close()
            

def create_user(user_data) -> Optional[Dict]:
    conn = None
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        check_query = f"""
            SELECT id FROM users WHERE email = '{user_data.email}'
        """

        logger.info("Checking email with query: %s", check_query)

        existing_user = cursor.execute(check_query).fetchone()

        if existing_user:
            logger.warning("Attempt to register existing email: %s", user_data.email)
            return None
        
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

        user = cursor.execute(
            f"SELECT id, fullname, email, address, is_admin FROM users WHERE id = {user_id}"
        ).fetchone()

        return dict(user) if user else None

    except sqlite3.IntegrityError as e:
        logger.warning("Integrity error while creating user: %s", str(e))
        return None

    except sqlite3.Error as e:
        logger.error("Database error while creating user: %s", str(e))
        return None

    except Exception:
        logger.exception("Unexpected error while creating user")
        return None

    finally:
        if conn:
            conn.close()