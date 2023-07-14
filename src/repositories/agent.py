from pathlib import Path
from typing import Optional

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.model import Agent, AgentRepository, Waypoint

AGENT_TOKEN_FILENAME = ".agent_token"
REPOSITORY_BASE_PATH = Path(__file__).parent.parent.parent
AGENT_TOKEN_PATH = REPOSITORY_BASE_PATH / AGENT_TOKEN_FILENAME


logger = structlog.get_logger()

class HttpAndFileAgentRepository(AgentRepository):
    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        agent_token = self._get_agent_token()
        if agent_token:
            logger.debug("Read existing agent from file", agent_token=agent_token)
            agent = self._get_existing_agent(agent_token)
            return agent
        else:
            return self._create_agent()

    def _get_agent_token(self) -> Optional[str]:
        if AGENT_TOKEN_PATH.exists():
            with open(AGENT_TOKEN_PATH, "r") as f:
                return f.read()
        return None

    def _get_existing_agent(self, agent_token: str) -> Agent:
        response = req.get(
            url = "https://api.spacetraders.io/v2/my/agent",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        headquarters = response.json()["data"]["headquarters"]
        logger.debug("Gotten info from existing agent",
                     agent=Agent(agent_token, headquarters))
        return Agent(agent_token, headquarters)


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
        headquarters = response.json()["data"]["headquarters"]
        agent = Agent(token, headquarters)
        logger.debug("Created a new agent", agent=agent)
        with open(AGENT_TOKEN_PATH, "w") as f:
            f.write(token)
        return agent


class InMemoryAgentRepository(AgentRepository):
    agent: Optional[Agent] = None

    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        if self.agent is None:
            self.agent = Agent(
                token = "DUMMY_TOKEN",
                headquarters = Waypoint("X1-YY2-ZZZZZ3")
            )
        return self.agent
