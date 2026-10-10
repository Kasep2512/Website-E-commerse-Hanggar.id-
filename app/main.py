from fastapi import FastAPI

app = FastAPI(title="Hanggar.id API")

@app.get("/")
def read_root():
    return {"message": "Hello dari API Hanggar.id!"}