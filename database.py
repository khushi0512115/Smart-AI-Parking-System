import sqlite3
import os

# 📁 Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "parking.db")


# -------------------------------
# 🧠 INITIALIZE DATABASE
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Logs table
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        free INTEGER,
        occupied INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# 📊 INSERT LOG
# -------------------------------
def insert_log(free, occupied):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO logs (free, occupied) VALUES (?, ?)",
        (free, occupied)
    )

    conn.commit()
    conn.close()


# -------------------------------
# 📈 GET LOGS (for analytics)
# -------------------------------
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT timestamp, free, occupied
        FROM logs
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    data = c.fetchall()
    conn.close()

    return data[::-1]