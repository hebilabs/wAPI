from app.core.database import get_db


def authenticate_user(username: str, password: str):

    conn = get_db()
    cursor = conn.cursor()

    ## sqli
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = cursor.execute(query).fetchone()

    return user