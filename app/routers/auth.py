from datetime import datetime, timedelta, timezone
import os

from fastapi import APIRouter, Depends, HTTPException, Response, status
from jose import jwt
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.database_dependencies import get_db
from app.models.user import User




def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=60)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

password_hash = PasswordHash.recommended()

class LoginRegisterRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: LoginRegisterRequest,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(User).where(User.username == request.username)
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    user = User(
        username=request.username,
        password_hash=password_hash.hash(request.password),
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}

@auth_router.post("/login")
def login(
    request: LoginRegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.username == request.username)
    )

    if (
        user is None
        or not password_hash.verify(
            request.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,      # True in production with HTTPS
        samesite="lax",
        max_age=3600,
    )

    return {"message": "Logged in"}