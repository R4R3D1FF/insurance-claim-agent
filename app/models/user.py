from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_file_access import UserFileAccess
    from app.models.user_agent_access import UserAgentAccess

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password_hash: Mapped[str]

    file_access: Mapped[list["UserFileAccess"]] = relationship(
        back_populates="user"
    )

    agent_access: Mapped[list["UserAgentAccess"]] = relationship(
        back_populates="user"
    )