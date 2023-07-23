
from src.domain.agent import Agent
from src.domain.waypoint import Waypoint
from src.orchestration.purchase_ship import (
    find_local_shipyard,
    list_available_ship_types,
)
from src.repositories.agent import InMemoryAgentRepository
from src.repositories.waypoint import InMemoryWaypoinyRepository


def test_find_a_shipyard() -> None:
    agent_1 = Agent("DUMMY_TOKEN", Waypoint("A1-BB2-WP001"))
    system_with_shipyard = {"A1-BB2": [
        Waypoint("coord1", ["NOT COOL", "TOO HOT", "I'M DYING HERE"]),
        Waypoint("coord2", ["COLD", "SO COLD", "IT'S LIKE HOTH ALL OVER AGAIN"]),
        Waypoint("coord3", ["MARKETPLACE", "SHIPYARD"]),
        ]
    }
    agent_2 = Agent("DUMMY_TOKEN", Waypoint("A2-BB3-WP001"))
    system_without_shipyard = {"A2-BB3": [
        Waypoint("single_planet", ["NOT A MARKETPLACE", "NOT A SHIPYARD"]),
        ]
    }

    agent_repo_1 = InMemoryAgentRepository(agent_1)
    agent_repo_2 = InMemoryAgentRepository(agent_2)
    waypoint_repo = InMemoryWaypoinyRepository(
            system_without_shipyard | system_with_shipyard)

    assert find_local_shipyard(
                agent_repo_1,
                waypoint_repo
            ) == \
            Waypoint("coord3",
                     ["MARKETPLACE", "SHIPYARD"]
            )
    assert find_local_shipyard(agent_repo_2, waypoint_repo) is None

def test_list_all_ship_types() -> None:
    agent_repo = InMemoryAgentRepository(Agent("DUMMY_TOKEN", Waypoint("A1-BB2-CCCC5")))
    shipyard = Waypoint("coord3", ["MARKETPLACE", "SHIPYARD"])
    system_with_shipyard = {"A1-BB2": [
        Waypoint("coord1", ["NOT COOL", "TOO HOT", "I'M DYING HERE"]),
        Waypoint("coord2", ["COLD", "SO COLD", "IT'S LIKE HOTH ALL OVER AGAIN"]),
        shipyard,
        ]
    }
    shipyards = {shipyard: {"BIG ASS SHIP", "SMALL SHIP", "BROKEN SHIP"}}
    waypoint_repo = InMemoryWaypoinyRepository(system_with_shipyard, shipyards)

    ship_types = list_available_ship_types(agent_repo, waypoint_repo, shipyard)

    assert ship_types == {"BIG ASS SHIP", "SMALL SHIP", "BROKEN SHIP"}
