from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.database_dependencies import get_db
from app.lib.jwt import verify_and_extract_payload_from_jwt
from app.models.user import User


def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    print("access_token", access_token)
    if access_token is None:
        return None
    
    payload = verify_and_extract_payload_from_jwt(access_token)

    user_id = payload["sub"]

    print("user_id", user_id)
    
    row = (
        db.execute(
            select(User.id, User.username)
            .where(User.id == user_id)
        )
        .mappings()
        .one_or_none()
    )

    if row is None:
        return None

    return row