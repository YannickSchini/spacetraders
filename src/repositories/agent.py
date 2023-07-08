from typing import Optional
from pathlib import Path
from src.domain.model import AgentRepository
from src.domain.model import Agent
import requests as req

AGENT_TOKEN_FILENAME = ".agent_token"
REPOSITORY_BASE_PATH = Path(__file__).parent.parent.parent
AGENT_TOKEN_PATH = REPOSITORY_BASE_PATH / AGENT_TOKEN_FILENAME

class HttpAndFileAgentRepository(AgentRepository):
    def get_agent(self) -> Agent:
        agent_token = self._get_agent_token()
        if agent_token:
            return Agent(agent_token)
        else:
            return self._create_agent()

    def _get_agent_token(self) -> Optional[str]:
        if AGENT_TOKEN_PATH.exists():
            with open(AGENT_TOKEN_PATH, "r") as f:
                return f.read()
        return None

    def _create_agent(self) -> Agent:
        data: str = '{"symbol": "YoShi", "faction": "COSMIC"}'
        response = req.post(
            url = "https://api.spacetraders.io/v2/register",
            headers = {"Content-Type": "application/json"},
            data = data,
        )
        token = response.json()["data"]["token"]
        with open(AGENT_TOKEN_PATH, "w") as f:
            f.write(token)
        return Agent(token)


class InMemoryAgentRepository(AgentRepository):
    agent: Optional[Agent] = None

    def get_agent(self) -> Agent:
        print("Before the if: ", self.agent)
        if self.agent is None:
            self.agent = Agent(
                token = "DUMMY_TOKEN",
            )
        print("After the if: ", self.agent)
        return self.agent
