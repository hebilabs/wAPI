import sqlite3
import os
from app.core.config import get_settings

settings = get_settings()

DB_NAME = settings.DATABASE_URL


def get_db():
    directory = os.path.dirname(DB_NAME)

    if directory: 
        os.makedirs(directory, exist_ok=True)

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
        email TEXT,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        image_url TEXT,
        internal_cost REAL
    );

    CREATE TABLE cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        image_url TEXT,
        quantity INTEGER
    );

    INSERT INTO users (email,password,is_admin)
    VALUES ('admin@mail.com','4dMin432.',1);

    INSERT INTO users (email,password,is_admin)
    VALUES ('user@mail.com','password',0);

    INSERT INTO products (name, description, price, image_url, internal_cost)
    VALUES 
    ('Green large T-Shirt',
    'Lightweight cotton t-shirt in vibrant orange tone, ideal for beach days and warm weather outfits.',
    1200,
    'https://images.pexels.com/photos/9604298/pexels-photo-9604298.jpeg?auto=compress&cs=tinysrgb&w=600',
    750),

    ('Flowers Linen Shirt',
    'Premium fleece hoodie with relaxed fit and warm inner lining, perfect for cold urban nights.',
    1800,
    'https://images.pexels.com/photos/8638697/pexels-photo-8638697.jpeg?auto=compress&cs=tinysrgb&w=600',
    1100),

    ('Slim Black Tshirt',
    'Minimalistic crop top with clean lines and soft fabric, designed for a modern cosmic aesthetic.',
    900,
    'https://images.pexels.com/photos/9558577/pexels-photo-9558577.jpeg?auto=compress&cs=tinysrgb&w=600',
    600),

    ('Slim Pink Tshirt',
    'Essential white t-shirt with tailored fit, breathable fabric and timeless casual look.',
    1100,
    'https://images.pexels.com/photos/9558568/pexels-photo-9558568.jpeg?auto=compress&cs=tinysrgb&w=600',
    700),

    ('Blue Sweater',
    'Deep green oversized shirt combining elegance and rebellious streetwear style.',
    1500,
    'https://images.pexels.com/photos/8437064/pexels-photo-8437064.jpeg?auto=compress&cs=tinysrgb&w=600',
    1000),

    ('Black Street Tshirt',
    'Modern black lightweight jacket with structured shoulders and contemporary street silhouette.',
    2500,
    'https://images.pexels.com/photos/6256326/pexels-photo-6256326.jpeg?auto=compress&cs=tinysrgb&w=600',
    1700),

    ('Pink Sweet Jacket',
    'Classic denim button-up shirt with soft washed texture, ideal for smart casual outfits.',
    1700,
    'https://images.pexels.com/photos/31594459/pexels-photo-31594459.jpeg?auto=compress&cs=tinysrgb&w=600',
    1200),

    ('1956-2018',
    'Neutral beige hoodie with relaxed fit and premium stitching for everyday comfort.',
    1900,
    'https://images.pexels.com/photos/5552600/pexels-photo-5552600.jpeg?auto=compress&cs=tinysrgb&w=600',
    1300),

    ('I Appreciate your advice',
    'Elegant sleeveless black top with minimalist cut, perfect for evening casual wear.',
    850,
    'https://images.pexels.com/photos/6256327/pexels-photo-6256327.jpeg?auto=compress&cs=tinysrgb&w=600',
    550),

    ('Lines Sweater',
    'Loose fit streetwear t-shirt with modern silhouette and breathable cotton blend.',
    1300,
    'https://images.pexels.com/photos/6105122/pexels-photo-6105122.jpeg?auto=compress&cs=tinysrgb&w=600',
    850),
                                                                  
    ('White Casual Jacket',
    'Loose fit streetwear t-shirt with modern silhouette and breathable cotton blend.',
    1300,
    'https://images.pexels.com/photos/8194927/pexels-photo-8194927.jpeg?auto=compress&cs=tinysrgb&w=600',
    850),
                                        
    ('Gray Hoodie',
    'Loose fit streetwear t-shirt with modern silhouette and breathable cotton blend.',
    1300,
    'https://images.pexels.com/photos/6995862/pexels-photo-6995862.jpeg?auto=compress&cs=tinysrgb&w=600',
    850),
                         
    ('Relax White Tshirt',
    'Loose fit streetwear t-shirt with modern silhouette and breathable cotton blend.',
    1300,
    'https://images.pexels.com/photos/4970991/pexels-photo-4970991.jpeg?auto=compress&cs=tinysrgb&w=600',
    850),
                                                         
    ('Cozzy Attire',
    'Loose fit streetwear t-shirt with modern silhouette and breathable cotton blend.',
    1300,
    'https://images.pexels.com/photos/34576869/pexels-photo-34576869.jpeg?auto=compress&cs=tinysrgb&w=600',
    850)                 
    """)

    conn.commit()
    conn.close()