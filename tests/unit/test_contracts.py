from typing import List

from src.domain.agent import Contract, Delivery
from src.domain.waypoint import Waypoint
from src.repositories.agent import InMemoryAgentRepository
from src.repositories.contract import InMemoryContractRepository

contracts = [
    Contract(
        contract_id="DUMMY_CONTRACT_1",
        delivery_details=[
            Delivery(
                merchandise="ROCK",
                destination=Waypoint("THERE"),
                units_required=100,
                units_fulfilled=0,
            ),
        ]
    ),
    Contract(
        contract_id="DUMMY_CONTRACT_2",
        delivery_details=[
            Delivery(
                merchandise="ROCK",
                destination=Waypoint("THERE"),
                units_required=10000,
                units_fulfilled=0,
            ),
            Delivery(
                merchandise="GOLD",
                destination=Waypoint("ALL_THE_WAY_OVER_THERE"),
                units_required=100,
                units_fulfilled=5,
            ),
        ]
    ),
]

def test_get_contracts_returns_contracts(contracts: List[Contract] = contracts) -> None:
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    contracts_repo = InMemoryContractRepository(contracts)
    agent = agent_repo.get_agent()

    assert contracts == agent.get_contracts(contracts_repo)

def test_accept_contract(contracts: List[Contract] = contracts) -> None:
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    contracts_repo = InMemoryContractRepository(contracts)
    agent = agent_repo.get_agent()
    contracts = agent.get_contracts(contracts_repo)

    agent.accept_contract(contracts[0].contract_id, contracts_repo)

