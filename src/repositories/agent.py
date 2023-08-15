import random
import string
from pathlib import Path
from typing import Optional

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.agent import Agent, AgentRepository
from src.domain.waypoint import Waypoint

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
        headquarters = Waypoint(response.json()["data"]["headquarters"])
        logger.debug("Gotten info from existing agent",
                     agent=Agent(agent_token, headquarters))
        return Agent(agent_token, headquarters)


    def _create_agent(self) -> Agent:
        data: str = '{"symbol": "YoShingy", "faction": "COSMIC"}'
        response = req.post(
            url = "https://api.spacetraders.io/v2/register",
            headers = {"Content-Type": "application/json"},
            data = data,
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        token = response.json()["data"]["token"]
        headquarters = Waypoint(response.json()["data"]["agent"]["headquarters"])
        agent = Agent(token, headquarters)
        logger.debug("Created a new agent", agent=agent)
        with open(AGENT_TOKEN_PATH, "w") as f:
            f.write(token)
        return agent


class InMemoryAgentRepository(AgentRepository):
    def __init__(self, agent: Agent):
        self.agent = agent

    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        return self.agent
    
    @staticmethod
    def create_agent_repo(
        token: str = "DUMMY_TOKEN",
        headquarters: str = "X1-YY2-ZZZZZ3"
    ) -> AgentRepository:
        return InMemoryAgentRepository(Agent(token, Waypoint(headquarters)))


class PureHttpAgentRepository(AgentRepository):
    def __init__(self) -> None:
        self.agent: Optional[Agent] = None

    def get_agent(self) -> Agent:
        logger.info("Getting the agent")
        if self.agent:
            return self.agent
        else:
            random_suffix = ''.join(random.choices(
                                            string.ascii_uppercase + string.digits,
                                            k=6
                                            )
                                    )
            return self._create_agent(agent_symbol="YoShi_" + random_suffix )

    def _create_agent(self, agent_symbol: str) -> Agent:
        data: str = '{"symbol": "%s", "faction": "COSMIC"}' % agent_symbol
        response = req.post(
            url = "https://api.spacetraders.io/v2/register",
            headers = {"Content-Type": "application/json"},
            data = data,
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        token = response.json()["data"]["token"]
        headquarters = Waypoint(response.json()["data"]["agent"]["headquarters"])
        agent = Agent(token, headquarters)
        logger.debug("Created a new agent", agent=agent)
        self.agent = agent
        return agent
