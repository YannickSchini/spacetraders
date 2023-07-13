from pathlib import Path
from typing import Optional

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.model import Agent, AgentRepository

AGENT_TOKEN_FILENAME = ".agent_token"
REPOSITORY_BASE_PATH = Path(__file__).parent.parent.parent
AGENT_TOKEN_PATH = REPOSITORY_BASE_PATH / AGENT_TOKEN_FILENAME


logger = structlog.get_logger()

class HttpAndFileAgentRepository(AgentRepository):
    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        agent_token = self._get_agent_token()
        if agent_token:
            logger.debug("Read existing agent from file", agent=Agent(agent_token))
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
        if response.status_code > 299:
            raise HTTPError(response.text)
        token = response.json()["data"]["token"]
        logger.debug("Created a new agent", agent=Agent(token))
        with open(AGENT_TOKEN_PATH, "w") as f:
            f.write(token)
        return Agent(token)


class InMemoryAgentRepository(AgentRepository):
    agent: Optional[Agent] = None

    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        if self.agent is None:
            self.agent = Agent(
                token = "DUMMY_TOKEN",
            )
        return self.agent
