import os
from fastapi import HTTPException
from jose import JWTError
import jwt

def verify_and_extract_payload_from_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
        )
    except JWTError:
        raise HTTPException(401)

    return payload