from app.core.database import get_db
from app.core.config import get_settings
from jose import jwt
from datetime import datetime, timedelta

settings = get_settings()

def authenticate_user(email: str, password: str):

    conn = get_db()
    cursor = conn.cursor()
    # sqli
    query = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
    user = cursor.execute(query).fetchone()
    print(f"Executed query: {query}")

    return user


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
