from abc import ABC
from dataclasses import dataclass



@dataclass
class Agent():
    token: str

    def __str__(self) -> str:
        return f"Agent with token {self.token}"


class AgentRepository(ABC):
    def get_agent(self) -> Agent:
        raise NotImplementedError
