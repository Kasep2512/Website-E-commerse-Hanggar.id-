# app/database.py
import sqlite3
from contextlib import contextmanager
import os

DB_PATH = "db/hanggar.db"

def get_connection():
    """
    Membuat koneksi ke SQLite dengan pengaturan performa dan keamanan. 
    """
    # Memastikan folder db/ ada
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # kolom berdasarkan nama

    # Pengaturan untuk performa dan keamanan SQLite
    conn.execute("PRAGMA journal_mode=WAL") # untuk performa baca/tulis
    conn.execute("PRAGMA foreign_keys=ON")  # Wajibkan Foreign Key
    conn.execute("PRAGMA busy_timeout=5000")# Tunggu maksimal 5 detik jika database terkunci
    return conn

@contextmanager
def get_db():
    """
    Context manager untuk menangani koneksi database.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()