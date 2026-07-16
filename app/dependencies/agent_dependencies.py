from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependencies import get_db
from app.repositories.agent_repository import AgentRepository
from app.services.agent_service import AgentService

def get_agent_repository(
    db: Session = Depends(get_db)
) -> AgentRepository:
    return AgentRepository(db)

def get_agent_service(repository: AgentRepository = Depends(get_agent_repository)):
    return AgentService(repository)