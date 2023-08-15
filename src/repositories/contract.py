from typing import List

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.agent import Contract, ContractRepository, Delivery
from src.domain.waypoint import Waypoint

logger = structlog.get_logger()


class HttpContractRepository(ContractRepository):
    def get_contracts(self, agent_token: str) -> List[Contract]:
        logger.info("Getting the contracts")
        response = req.get(
            url = "https://api.spacetraders.io/v2/my/contracts",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        contracts = []
        for raw_contract in response.json()["data"]:
            deliveries = []
            for raw_delivery_details in raw_contract["terms"]["deliver"]:
                deliveries.append(
                    Delivery(
                        merchandise=raw_delivery_details["tradeSymbol"],
                        destination=Waypoint(raw_delivery_details["destinationSymbol"]),
                        units_required=raw_delivery_details["unitsRequired"],
                        units_fulfilled=raw_delivery_details["unitsFulfilled"]
                    )
                )
            contracts.append(
                Contract(
                    contract_id=raw_contract["id"],
                    delivery_details=deliveries,
                )
            )
        return contracts

    def accept_contract(self, contract_id: str, agent_token: str) -> None:
        logger.info("Accepting the contract", contract_id=contract_id)
        req.post(
            url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )

class InMemoryContractRepository(ContractRepository):
    def __init__(self) -> None:
        self.contracts: List[Contract] = []

    def get_contracts(self, agent_token: str) -> List[Contract]:
        logger.info("Getting the contracts")
        return self.contracts

    def accept_contract(self, contract_id: str, agent_token: str) -> None:
        logger.info("Accepting the contract", contract_id=contract_id)
        if contract_id in [contract.contract_id for contract in self.contracts]:
            return None
        else:
            raise ValueError(f"Contract ID {contract_id} does not exist.")

    def append_contract_to_repo(
        self,
        contract_id: str = "DUMMY_CONTRACT_1",
        merchandise: str = "ROCK",
        destination: str = "THERE",
        units_required: int = 100,
        units_fulfilled: int = 0
    ) -> None:
        self.contracts.append(
            Contract(
                contract_id=contract_id,
                delivery_details=[
                    Delivery(
                        merchandise=merchandise,
                        destination=Waypoint(destination),
                        units_required=units_required,
                        units_fulfilled=units_fulfilled,
                    )
                ]
            )
        )

def create_in_memory_contract_repo() -> InMemoryContractRepository:
    repo = InMemoryContractRepository()
    repo.append_contract_to_repo()
    return repo
