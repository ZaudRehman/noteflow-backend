from fastapi import APIRouter, HTTPException, Body
import bcrypt
from typing import Annotated
from datetime import datetime
from app.models import get_user_by_email, insert_user
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(email: Annotated[str, Body()], password: Annotated[str, Body()]):
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = {
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now()
    }
    insert_user(user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(email: Annotated[str, Body()], password: Annotated[str, Body()]):
    user = get_user_by_email(email)
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "user_id": str(user["_id"])}