from typing import Optional, Set

from src.domain.agent import AgentRepository
from src.domain.waypoint import Waypoint, WaypointRepository
from src.repositories.agent import HttpAndFileAgentRepository
from src.repositories.waypoint import HttpWaypointRepository


def find_local_shipyard(agent_repo: AgentRepository,
                        waypoint_repo: WaypointRepository) -> Optional[Waypoint]:
    agent = agent_repo.get_agent()
    home_system = "-".join(agent.headquarters.waypoint.split("-")[0:2])
    waypoints = waypoint_repo.get_waypoints_in_system(home_system, agent.token)

    for wp in waypoints:
        if "SHIPYARD" in wp.traits:
            return wp
    return None

def list_available_ship_types(agent_repo: AgentRepository,
                              waypoint_repo: WaypointRepository,
                              shipyard: Waypoint) -> Set[str]:
    agent = agent_repo.get_agent()
    return waypoint_repo.list_available_ship_types(shipyard, agent.token)


if __name__ == "__main__":
    agent_repo = HttpAndFileAgentRepository()
    agent = agent_repo.get_agent()
    waypoint_repo = HttpWaypointRepository()
    shipyard = find_local_shipyard(agent_repo, waypoint_repo)
    if shipyard:
        ship_types = list_available_ship_types(agent_repo, waypoint_repo, shipyard)
        print(ship_types)

# 2. Purchase a ship
# 2.a. List all available ship types in a shipyard => OK !
# 2.b Buy the right ship from the shipyard
# (or raise a Domain exception if we don't have enough money)
# ==> Can be done with constants and strings for now, no need for complex logic
