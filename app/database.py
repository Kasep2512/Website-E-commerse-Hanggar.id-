# app/database.py
import sqlite3
import os

DB_PATH = "db/hanggar.db"

def get_connection():
    """
    Membuat koneksi ke SQLite dengan pengaturan performa dan keamanan.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

# HAPUS @contextmanager dari sini
def get_db():
    """
    Generator untuk menangani koneksi database di FastAPI.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()