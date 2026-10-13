import sqlite3

DATABASE = "lab.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL
        )
    """)

    users = [
        ("admin", "adminpass"),
        ("abdul", "abdul321"),
        ("boobs", "greatboobs"),
        ("cyber", "staySaf3"),
    ]

    conn.executemany("""
        INSERT INTO users (username, password)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE username = ?
        )
    """, [(username, password, username)
          for username, password in users])

    products = [
        (
            "Wireless Mouse",
            "Accessories",
            8500.00,
            "A reliable wireless mouse for everyday computing."
        ),
        (
            "Mechanical Keyboard",
            "Accessories",
            28500.00,
            "A mechanical keyboard designed for comfortable typing."
        ),
        (
            "USB-C Hub",
            "Accessories",
            19500.00,
            "A compact hub with multiple connectivity options."
        ),
        (
            "Laptop Stand",
            "Workspace",
            12000.00,
            "An adjustable stand for a comfortable workspace."
        ),
        (
            "HD Webcam",
            "Electronics",
            22000.00,
            "An HD webcam for video calls and online classes."
        ),
        (
            "Headphones",
            "Audio",
            17500.00,
            "Over-ear headphones for everyday listening."
        ),
    ]

    conn.executemany("""
        INSERT INTO products (name, category, price, description)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM products WHERE name = ?
        )
    """, [(*product, product[0]) for product in products])

    conn.commit()
    conn.close()

    print("Database initialized successfully.")
    print("Users and products tables are ready.")


if __name__ == "__main__":
    init_db()
