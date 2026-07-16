from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_agent_access import UserAgentAccess
from app.models.user_file_access import UserFileAccess


def has_file_access(
    db: Session,
    user_id: int,
    file_id: int,
) -> bool:
    return (
        db.execute(
            select(UserFileAccess.user_id).where(
                UserFileAccess.user_id == user_id,
                UserFileAccess.file_id == file_id,
            )
        ).scalar_one_or_none()
        is not None
    )

def has_agent_access(
    db: Session,
    user_id: int,
    agent_id: int,
) -> bool:
    return (
        db.execute(
            select(UserAgentAccess.user_id).where(
                UserAgentAccess.user_id == user_id,
                UserAgentAccess.agent_id == agent_id,
            )
        ).scalar_one_or_none()
        is not None
    )