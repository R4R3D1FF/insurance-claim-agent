from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.agent import Agent


class UserAgentAccess(Base):
    __tablename__ = "user_agent_access"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id"),
        primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="agent_access")
    agent: Mapped["Agent"] = relationship(back_populates="accesses")