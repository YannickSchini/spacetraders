from src.domain.agent import Agent, Contract
from src.domain.waypoint import Waypoint
from src.orchestration.create_agent import create_agent
from src.orchestration.manage_contracts import get_contracts
from src.orchestration.purchase_ship import (
    buy_ship,
    find_local_shipyard,
    list_available_ship_types,
)
from src.repositories.agent import PureHttpAgentRepository
from src.repositories.contract import HttpContractRepository
from src.repositories.waypoint import HttpWaypointRepository


def test_run_tutorial() -> None:
    # Initialization of the required dependencies
    agent_repo = PureHttpAgentRepository()
    contracts_repo = HttpContractRepository()
    waypoint_repo = HttpWaypointRepository()

    # Agent creation
    agent = create_agent(agent_repo)

    assert isinstance(agent, Agent)
    assert agent.token is not None

    # Contract management
    contracts = get_contracts(agent_repo=agent_repo, contracts_repo=contracts_repo)

    assert len(contracts) > 0
    assert isinstance(contracts[0], Contract)

    first_contract_id = contracts[0].contract_id
    assert first_contract_id is not None

    agent.accept_contract(first_contract_id, contracts_repo)

    # Buy a ship
    shipyard = find_local_shipyard(agent_repo, waypoint_repo)
    assert isinstance(shipyard, Waypoint)
    assert "SHIPYARD" in shipyard.traits

    available_ship_types = list_available_ship_types(agent_repo,
                                                     waypoint_repo,
                                                     shipyard)
    assert len(available_ship_types) > 0
    assert "SHIP_MINING_DRONE" in available_ship_types

    buy_ship(agent_repo, waypoint_repo, shipyard, "SHIP_MINING_DRONE")
