from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies.agent_dependencies import get_agent_service
from app.dependencies.database_dependencies import get_db
from app.dependencies.file_dependencies import get_file_service
from app.dependencies.user_dependencies import get_current_user
from app.lib.access_checker import has_agent_access, has_file_access
from app.models.user import User
from app.services.agent_service import AgentService
from app.services.file_service import FileService
from app.services.policy_checker import PolicyChecker, Reflection

agent_router = APIRouter(prefix="/agent", tags=["Agent"])

class MessageRequest(BaseModel):
    claim_id: int

MessageResponse = Reflection

@agent_router.post(
    "/{agent_id}/message",
    response_model = MessageResponse,
)
def check_claim_validity(
    agent_id: str, 
    message_request: MessageRequest,
    file_service: FileService = Depends(get_file_service),
    agent_service: AgentService = Depends(get_agent_service),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    
    id = message_request.claim_id

    print("current_user", current_user)

    if not current_user or not has_file_access(db, current_user.id, id) or not has_agent_access(db, current_user.id, agent_id):
        raise HTTPException(403, "Forbidden")
    
    claim_file_path = file_service.get_path(id)
    
    rule_policy_path = agent_service.get_policy_path(agent_id)
    
    policy_checker = PolicyChecker(rule_policy_path)
    
    resp = policy_checker.check_validity(claim_file_path)

    return resp