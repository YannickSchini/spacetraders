from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.domain.waypoint import Waypoint


@dataclass
class Delivery():
    merchandise: str
    destination: Waypoint
    units_required: int
    units_fulfilled: int

@dataclass
class Contract():
    contract_id: str
    delivery_details: List[Delivery]

    def __str__(self) -> str:
        return f"Contract with ID {self.contract_id}"

class ContractRepository(ABC):
    @abstractmethod
    def get_contracts(self, agent_token: str) -> List[Contract]:
        raise NotImplementedError

    @abstractmethod
    def accept_contract(self, contract_id: str, agent_token: str) -> None:
        raise NotImplementedError

class Agent():
    def __init__(self, token: str, headquarters: Waypoint) -> None:
        self.token = token
        self.headquarters = headquarters

    def __str__(self) -> str:
        return f"Agent with token {self.token}"

    def get_contracts(self, contract_repository: ContractRepository) -> List[Contract]:
        return contract_repository.get_contracts(self.token)

    def accept_contract(self,
                        contract_id: str,
                        contract_repository: ContractRepository
                        ) -> None:
        contract_repository.accept_contract(
            contract_id=contract_id,
            agent_token=self.token
        )

class AgentRepository(ABC):
    @abstractmethod
    def get_agent(self) -> Agent:
        raise NotImplementedError
