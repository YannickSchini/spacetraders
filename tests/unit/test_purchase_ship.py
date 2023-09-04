from src.domain.waypoint import Waypoint
from src.orchestration.purchase_ship import (
    find_local_shipyard,
    list_available_ship_types,
)
from src.repositories.agent import InMemoryAgentRepository
from src.repositories.system import InMemorySystemRepository


def test_find_an_existing_shipyard_in_the_local_system() -> None:
    system_with_shipyard = InMemorySystemRepository()
    system = "X1-YY2"
    system_with_shipyard.add_waypoint(
        waypoint_id=system+"-CCCC3",
        traits=["NOT COOL", "TOO HOT", "I'M DYING HERE"]
    )
    system_with_shipyard.add_waypoint(
        waypoint_id=system+"-DDDD4",
        traits=["COLD", "SO COLD", "IT'S LIKE HOTH ALL OVER AGAIN"]
    )
    system_with_shipyard.add_waypoint(
        waypoint_id=system+"-EEEE5",
        traits=["MARKETPLACE", "SHIPYARD"]
    )
    agent_repo = InMemoryAgentRepository.create_agent_repo()

    assert find_local_shipyard(
                agent_repo,
                system_with_shipyard
            ) == \
            Waypoint("X1-YY2-EEEE5",
                     ["MARKETPLACE", "SHIPYARD"]
            )

def test_system_repo() -> None:
    system_1 = InMemorySystemRepository()
    system_2 = InMemorySystemRepository()
    system_2.add_waypoint()

    assert system_1.systems != system_2.systems


# def test_find_a_shipyard_returns_none_when_no_shipyard_exists_locally() -> None:
#     system_without_shipyard = InMemorySystemRepository()
#     system_without_shipyard.add_waypoint()
#     agent_repo = InMemoryAgentRepository.create_agent_repo()

#     assert find_local_shipyard(agent_repo, system_without_shipyard) is None

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
