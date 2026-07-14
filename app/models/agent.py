from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.file import File

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    policy_file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        nullable=False
    )

    policy_file: Mapped[File] = relationship()