from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.agent_dependencies import get_agent_service
from app.dependencies.file_dependencies import get_file_service
from app.services.agent_service import AgentService
from app.services.file_service import FileService
from app.services.policy_checker import PolicyChecker, Reflection

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class MessageRequest(BaseModel):
    claim_id: str

MessageResponse = Reflection

@chatbot_router.post(
    "/{agent_id}/message/",
    response_model = MessageResponse,
)
def check_claim_validity(
    agent_id: str, 
    message_request: MessageRequest,
    file_service: FileService = Depends(get_file_service),
    agent_service: AgentService = Depends(get_agent_service)
):
    id = message_request.claim_id
    claim_file_path = file_service.get_path(id)
    
    rule_policy_path = agent_service.get_policy_path()
    
    policy_checker = PolicyChecker(rule_policy_path)
    
    resp = policy_checker.check_validity(claim_file_path)

    return resp