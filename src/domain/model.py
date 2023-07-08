from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class Delivery():
    merchandise: str
    destination: str
    units_required: int
    units_fulfilled: int

@dataclass
class Contract():
    contract_id: str
    delivery_details: List[Delivery]

    def __str__(self) -> str:
        return f"Contract with ID {self.contract_id}"

class ContractRepository(ABC):
    def get_contracts(self, agent_token: str) -> List[Contract]:
        raise NotImplementedError

    def accept_contract(self, contract_id: str, agent_token: str) -> None:
        raise NotImplementedError

@dataclass
class Agent():
    token: str

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
    def get_agent(self) -> Agent:
        raise NotImplementedError
