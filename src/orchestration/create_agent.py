from src.domain.model import Agent, AgentRepository
from src.repositories.agent import HttpAndFileAgentRepository

def create_agent(agent_repo: AgentRepository) -> Agent:
    agent = agent_repo.get_agent()
    # print(agent)
    return agent


if __name__ == "__main__":
    agent_repo = HttpAndFileAgentRepository()
    create_agent(agent_repo)
