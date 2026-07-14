from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.models.base import Base

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filesystem_path: Mapped[str]