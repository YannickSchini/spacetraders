from src.orchestration.create_agent import create_agent
from src.repositories.agent import InMemoryAgentRepository

def test_create_agent_returns_token() -> None:
    agent_repo = InMemoryAgentRepository()
    agent = create_agent(agent_repo)
    assert agent.token == "DUMMY_TOKEN"
