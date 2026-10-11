import sqlite3

# Buka koneksi ke database
conn = sqlite3.connect("db/hanggar.db")

# Hapus tabel kyc_verifications yang strukturnya salah
conn.execute("DROP TABLE IF EXISTS kyc_verifications")
conn.commit()
conn.close()

print("Tabel kyc_verifications berhasil dihapus!")