from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_file_access import UserFileAccess

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filesystem_path: Mapped[str]

    accesses: Mapped["UserFileAccess"] = relationship(back_populates="file")