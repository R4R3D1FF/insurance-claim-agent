from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.file import File

if TYPE_CHECKING:
    from app.models.user_agent_access import UserAgentAccess

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    policy_file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        nullable=False
    )

    policy_file: Mapped[File] = relationship()

    accesses: Mapped["UserAgentAccess"] = relationship(back_populates="agent")