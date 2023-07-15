from src.domain.agent import Agent, AgentRepository
from src.logging import configure_logger
from src.repositories.agent import HttpAndFileAgentRepository


def create_agent(agent_repo: AgentRepository) -> Agent:
    agent = agent_repo.get_agent()
    return agent


if __name__ == "__main__":
    configure_logger()
    agent_repo = HttpAndFileAgentRepository()
    agent = create_agent(agent_repo)
    print(agent)
