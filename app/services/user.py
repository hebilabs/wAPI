from app.core.database import get_db

def get_user_by_id(user_id: int):
    conn = get_db()
    return conn.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()


def create_user(user_data):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO users (email,password,is_admin)
        VALUES ('{user_data.email}','{user_data.password}',{user_data.is_admin})
    """)

    conn.commit()