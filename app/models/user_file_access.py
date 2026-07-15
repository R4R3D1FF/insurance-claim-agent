from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.file import File
from app.models.user import User


class UserFileAccess(Base):
    __tablename__ = "user_file_access"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        primary_key=True,
    )

    user: Mapped[User] = relationship(back_populates="file_accesses")
    file: Mapped[File] = relationship(back_populates="accesses")