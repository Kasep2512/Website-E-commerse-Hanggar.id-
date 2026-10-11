# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        tier_id: int = payload.get("tier")
        if user_id is None or tier_id is None:
            raise HTTPException(status_code=401, detail="Token tidak valid")
        return {"id": user_id, "tier": tier_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sesi telah berakhir, silahkan login kembali")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

def require_tier_1(current_user: dict = Depends(get_current_user)):
    """Memastikan user minimal Tier 1 (Penjual terverifikasi)"""
    # Asumsi: id 1 = Tier 0, id 2 = Tier 1, id 3 = Tier 2, id 4 = Admin
    if current_user["tier"] < 2:
        raise HTTPException(status_code=403, detail="Akses ditolak: Anda harus memverifikasi KYC untuk menjadi si Penjual")
    return current_user

def require_admin(current_user: dict = Depends(get_current_user)):
    """Memastikan user adalah Admin"""
    if current_user["tier"] != 4:
        raise HTTPException(status_code=403, detail="Akses ditolak: Fitur khusus Administrator")
    return current_user