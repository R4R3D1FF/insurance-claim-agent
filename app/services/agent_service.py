from app.repositories.agent_repository import AgentRepository


class AgentService:
    def __init__(self, repository: AgentRepository):
        self.repository = repository

    def get_policy_path(self, agent_id: int) -> str:
        print("agent_id", agent_id)
        agent = self.repository.get(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        return agent.policy_file.filesystem_path