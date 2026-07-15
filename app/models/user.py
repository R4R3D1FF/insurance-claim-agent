from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user_file_access import UserFileAccess

class User(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password_hash: Mapped[str]

    file_accesses: Mapped[list[UserFileAccess]] = relationship(
        back_populates="user"
    )