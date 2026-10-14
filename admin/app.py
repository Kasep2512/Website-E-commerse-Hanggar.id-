import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

# Tambahkan path root agar bisa membaca fungsi hash dari app/auth.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.auth import verify_password

DB_PATH = "db/hanggar.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Admin Hanggar.id", layout="wide")
st.title("🛡️ Panel Admin Hanggar.id")

# --- SISTEM LOGIN ADMIN ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.subheader("Login Administrator")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Masuk"):
        conn = get_db()
        user = conn.execute("SELECT id, password_hash, tier_id FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if user and verify_password(user["password_hash"], password):
            if user["tier_id"] == 4: # 4 adalah ID untuk Admin
                st.session_state.admin_logged_in = True
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Akses Ditolak: Anda bukan Admin.")
        else:
            st.error("Email atau password salah.")
    st.stop() # Hentikan eksekusi kode di bawah ini jika belum login

# --- DASHBOARD ADMIN (Jika sudah login) ---
if st.button("Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

tab1, tab2 = st.tabs(["📋 Antrean KYC", "📦 Master Katalog"])

# TAB 1: Manajemen KYC
with tab1:
    st.header("Antrean Verifikasi Penjual")
    conn = get_db()
    # Ambil data KYC yang masih pending
    kyc_data = conn.execute("""
        SELECT k.id as kyc_id, u.id as user_id, u.email, u.full_name, k.ktp_filename, k.selfie_filename 
        FROM kyc_verifications k 
        JOIN users u ON k.user_id = u.id 
        WHERE k.status = 'pending'
    """).fetchall()
    
    if not kyc_data:
        st.info("Tidak ada antrean KYC saat ini.")
    else:
        for row in kyc_data:
            with st.expander(f"Pengajuan dari: {row['full_name']} ({row['email']})"):
                col1, col2 = st.columns(2)
                try:
                    # Menampilkan gambar dari folder private
                    col1.image(f"private/kyc/{row['ktp_filename']}", caption="Foto KTP", use_container_width=True)
                    col2.image(f"private/kyc/{row['selfie_filename']}", caption="Swafoto", use_container_width=True)
                except Exception as e:
                    st.error(f"Gagal memuat gambar: {e}")
                
                col_btn1, col_btn2 = st.columns(2)
                if col_btn1.button("✅ Setujui", key=f"approve_{row['kyc_id']}"):
                    # Update status KYC dan naikkan tier user ke Tier 1 (ID 2)
                    conn.execute("UPDATE kyc_verifications SET status = 'approved' WHERE id = ?", (row['kyc_id'],))
                    conn.execute("UPDATE users SET tier_id = 2 WHERE id = ?", (row['user_id'],))
                    conn.commit()
                    st.success("Pengajuan disetujui!")
                    st.rerun()
                    
                if col_btn2.button("❌ Tolak", key=f"reject_{row['kyc_id']}"):
                    conn.execute("UPDATE kyc_verifications SET status = 'rejected' WHERE id = ?", (row['kyc_id'],))
                    conn.commit()
                    st.warning("Pengajuan ditolak.")
                    st.rerun()
    conn.close()

# TAB 2: Manajemen Katalog
with tab2:
    st.header("Master Katalog Gundam")
    conn = get_db()
    
    with st.form("form_tambah_katalog"):
        st.subheader("Tambah Produk Baru")
        c1, c2 = st.columns(2)
        nama = c1.text_input("Nama (ex: RX-78-2 Gundam)")
        seri = c2.text_input("Seri (ex: Mobile Suit Gundam)")
        grade = c1.selectbox("Grade", ["HG", "RG", "MG", "PG", "SD", "Lainnya"])
        skala = c2.selectbox("Skala", ["1/144", "1/100", "1/60", "Non-scale"])
        msrp = st.number_input("Harga Rilis (MSRP JPY)", min_value=0, step=100)
        
        if st.form_submit_button("Simpan ke Katalog"):
            if nama and seri:
                conn.execute(
                    "INSERT INTO catalog_products (name, series, grade, scale, msrp_jpy) VALUES (?, ?, ?, ?, ?)",
                    (nama, seri, grade, skala, msrp)
                )
                conn.commit()
                st.success("Produk berhasil ditambahkan!")
            else:
                st.error("Nama dan Seri wajib diisi.")
                
    st.divider()
    st.subheader("Daftar Katalog Saat Ini")
    # Tampilkan katalog menggunakan Pandas DataFrame (tampilan tabel yang rapi di Streamlit)
    df_katalog = pd.read_sql_query("SELECT id, name, series, grade, scale, msrp_jpy FROM catalog_products", conn)
    st.dataframe(df_katalog, use_container_width=True)
    conn.close()