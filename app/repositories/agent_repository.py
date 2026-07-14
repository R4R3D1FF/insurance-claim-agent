from sqlalchemy.orm import Session

from app.models.agent import Agent


class AgentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, agent_id: int) -> Agent:
        self.db.get(Agent, agent_id)

    def create(self):
        agent = Agent()
        self.db.add(agent)
        
        self.db.commit()
        self.db.refresh(agent)

        return agent
    
    def set_policy_file(
        self,
        agent_id: int,
        policy_file_id: int
    ) -> Agent:
        agent = self.get(agent_id)
        if agent is None:
            raise ValueError("Agent not found")
        agent.policy_file_id = policy_file_id
        self.db.commit()

        return agent