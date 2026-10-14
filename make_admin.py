import sqlite3

email_admin = input("Masukkan email akun yang ingin dijadikan Admin: ")

conn = sqlite3.connect("db/hanggar.db")
cursor = conn.cursor()

# cek email
cursor.execute("SELECT id FROM users WHERE email = ?", (email_admin,))
user = cursor.fetchone()

if user:
    # ubah tier_id (admin)
    cursor.execute("UPDATE users SET tier_id = 4 WHERE email = ?", (email_admin,))
    conn.commit()
    print(f"Berhasil! Akun {email_admin} sekarang adalah Admin.")
else:
    print("Email tidak ditemukan di dalam database.")

conn.close()