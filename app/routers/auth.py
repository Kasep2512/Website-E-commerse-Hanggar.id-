# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token
import sqlite3

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: RegisterRequest, db: sqlite3.Connection = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    try:
        cursor = db.execute(
            "INSERT INTO users (email, password_hash, full_name, tier_id) VALUES (?, ?, ?, 1)",
            (user.email, hashed_pw, user.full_name)
        )
        db.commit()
        return {"message": "Registrasi berhasil", "user_id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

@router.post("/login")
def login(user: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT id, email , password_hash, tier_id FROM users WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()

    if not db_user or not verify_password(db_user["password_hash"], user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = create_access_token({"sub": db_user["email"], "id": db_user["id"], "tier": db_user["tier_id"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/discord/login")
def discord_login_mock():
    return {"message": "URL Redirect ke Discord OAuth2 akan dibuat di sini"}