from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth

app = FastAPI(title="Hanggar.id API")

app.include_router(auth.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")