# db/migrate.py
import sqlite3
import os

DB_PATH = "db/hanggar.db"

def run_migrations():
    print("Memulai proses migrasi...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Hubungkan tanpa dict factory untuk eksekusi skrip mentah
    conn = sqlite3.connect(DB_PATH)

    try:
        # Eksekusi 001_initial_schema.sql
        print("Menjalankan 001_initial_schema.sql...")
        with open("db/001_initial_schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            
        # Eksekusi 002_kyc_schema.sql (TAMBAHAN BARU)
        print("Menjalankan 002_kyc_schema.sql...")
        with open("db/002_kyc_schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        # Masukkan data bawaan untuk Tiers jika belum ada
        conn.execute("INSERT OR IGNORE INTO tiers (id, name, description) VALUES (1, 'Tier 0', 'Pembeli')")
        conn.execute("INSERT OR IGNORE INTO tiers (id, name, description) VALUES (2, 'Tier 1', 'Penjual Terverifikasi')")
        conn.execute("INSERT OR IGNORE INTO tiers (id, name, description) VALUES (3, 'Tier 2', 'Trusted Builder')")
        conn.execute("INSERT OR IGNORE INTO tiers (id, name, description) VALUES (4, 'Admin', 'Administrator Sistem')")
        
        conn.commit()
        print("Migrasi selesai dengan sukses!")

    except Exception as e:
        print(f"Error saat migrasi: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migrations()