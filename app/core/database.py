import sqlite3
import os
from app.core.config import get_settings

settings = get_settings()

DB_NAME = settings.DATABASE_URL


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if os.path.exists(DB_NAME):
        return

    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        internal_cost REAL
    );

    CREATE TABLE cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    );

    INSERT INTO users (username,password,is_admin)
    VALUES ('admin','admin123',1);

    INSERT INTO users (username,password,is_admin)
    VALUES ('user','password',0);

    INSERT INTO products (name,description,price,internal_cost)
    VALUES ('Laptop','Gaming Laptop',1200,800);
    """)

    conn.commit()
    conn.close()