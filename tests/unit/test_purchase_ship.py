from src.domain.waypoint import Waypoint
from src.orchestration.purchase_ship import (
    find_local_shipyard,
    list_available_ship_types,
)
from src.repositories.agent import InMemoryAgentRepository
from src.repositories.system import InMemorySystemRepository


def test_find_an_existing_shipyard_in_the_local_system() -> None:
    system_with_shipyard = {"X1-YY2": [
        Waypoint("coord1", ["NOT COOL", "TOO HOT", "I'M DYING HERE"]),
        Waypoint("coord2", ["COLD", "SO COLD", "IT'S LIKE HOTH ALL OVER AGAIN"]),
        Waypoint("coord3", ["MARKETPLACE", "SHIPYARD"]),
        ]
    }
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    waypoint_repo = InMemorySystemRepository(system_with_shipyard)

    assert find_local_shipyard(
                agent_repo,
                waypoint_repo
            ) == \
            Waypoint("coord3",
                     ["MARKETPLACE", "SHIPYARD"]
            )


def test_find_a_shipyard_returns_none_when_no_shipyard_exists_locally() -> None:
    system_without_shipyard = {"X1-YY2": [
        Waypoint("single_planet", ["NOT A MARKETPLACE", "NOT A SHIPYARD"]),
        ]
    }

    agent_repo = InMemoryAgentRepository.create_agent_repo()
    waypoint_repo = InMemorySystemRepository(system_without_shipyard)

    assert find_local_shipyard(agent_repo, waypoint_repo) is None

def test_list_all_ship_types_from_a_local_shipyard() -> None:
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    shipyard = Waypoint("coord3", ["MARKETPLACE", "SHIPYARD"])
    system_with_shipyard = {"X1-YY2": [
        Waypoint("coord1", ["NOT COOL", "TOO HOT", "I'M DYING HERE"]),
        Waypoint("coord2", ["COLD", "SO COLD", "IT'S LIKE HOTH ALL OVER AGAIN"]),
        shipyard,
        ]
    }
    shipyards = {shipyard: {"BIG ASS SHIP", "SMALL SHIP", "BROKEN SHIP"}}
    waypoint_repo = InMemorySystemRepository(system_with_shipyard, shipyards)

    ship_types = list_available_ship_types(agent_repo, waypoint_repo, shipyard)

    assert ship_types == {"BIG ASS SHIP", "SMALL SHIP", "BROKEN SHIP"}
