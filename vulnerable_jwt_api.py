from fastapi import FastAPI, HTTPException, Header
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="JWT Auth Security Lab - Vulnerable Version")

SECRET_KEY = "secret123"  # intentionally weak
ALGORITHM = "HS256"

users = {
    "alice": {"username": "alice", "password": "password123", "role": "user"},
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
}

def create_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def root():
    return {"message": "Vulnerable JWT API running"}

@app.post("/login")
def login(username: str, password: str):
    user = users.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user["username"], user["role"])
    return {"access_token": token}

@app.get("/profile")
def profile(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    return {
        "username": payload["sub"],
        "role": payload["role"]
    }

@app.get("/admin")
def admin_panel(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return {"message": "Welcome to the admin panel"}