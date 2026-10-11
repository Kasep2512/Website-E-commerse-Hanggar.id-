# app/routers/users.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.dependencies import get_current_user
from app.database import get_db
import sqlite3
import os
import uuid

router = APIRouter(prefix="/api/users", tags=["users"])

UPLOAD_DIR = "private/kyc"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/verify-kyc")
async def upload_kyc(
    ktp: UploadFile = File(...),
    selfie: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    # cek user apakah sudah pernah melakukan submit KYC
    cursor = db.execute("SELECT status FROM kyc_verifications WHERE user_id = ?", (current_user["id"],))
    existing = cursor.fetchone()
    if existing and existing["status"] in ["pending", "approved"]:
        raise HTTPException(status_code=400, detail="KYC sudah diajukan atau sudah disetujui")

    # Generate nama file acak untuk keamanan
    ktp_ext = ktp.filename.split(".")[-1]
    selfie_ext = selfie.filename.split(".")[-1]
    ktp_filename = f"{current_user['id']}_ktp_{uuid.uuid4().hex[:8]}.{ktp_ext}"
    selfie_filename = f"{current_user['id']}_selfie_{uuid.uuid4().hex[:8]}.{selfie_ext}"

    # Simpan file secara lokal ke folder private
    with open(os.path.join(UPLOAD_DIR, ktp_filename), "wb") as buffer:
        buffer.write(await ktp.read())
    with open(os.path.join(UPLOAD_DIR, selfie_filename), "wb") as buffer:
        buffer.write(await selfie.read())

    # Catat ke database
    db.execute(
        "INSERT INTO kyc_verifications (user_id, ktp_filename, selfie_filename) VALUES (?, ?, ?)",
        (current_user["id"], ktp_filename, selfie_filename)
    )
    db.commit()

    return {"message": "Dokumen KYC berhasil diunggah. Menunggu persetujuan Admin."}