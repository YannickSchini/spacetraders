from typing import Optional, Set

from src.domain.agent import AgentRepository
from src.domain.waypoint import SystemRepository, Waypoint
from src.repositories.agent import HttpAndFileAgentRepository
from src.repositories.system import HttpSystemRepository


def find_local_shipyard(agent_repo: AgentRepository,
                        waypoint_repo: SystemRepository) -> Optional[Waypoint]:
    agent = agent_repo.get_agent()
    home_system = "-".join(agent.headquarters.waypoint.split("-")[0:2])
    system = waypoint_repo.get_waypoints_in_system(home_system, agent.token)

    for wp in system.waypoints:
        if "SHIPYARD" in wp.traits:
            return wp
    return None

def list_available_ship_types(agent_repo: AgentRepository,
                              waypoint_repo: SystemRepository,
                              shipyard: Waypoint) -> Set[str]:
    agent = agent_repo.get_agent()
    return waypoint_repo.list_available_ship_types(shipyard, agent.token)

def buy_ship(agent_repo: AgentRepository,
            waypoint_repo: SystemRepository,
             shipyard: Waypoint,
             ship_type: str) -> None:
    agent = agent_repo.get_agent()
    waypoint_repo.buy_ship(shipyard=shipyard,
                           ship_type=ship_type,
                           agent_token=agent.token)


if __name__ == "__main__":
    agent_repo = HttpAndFileAgentRepository()
    agent = agent_repo.get_agent()
    waypoint_repo = HttpSystemRepository()
    shipyard = find_local_shipyard(agent_repo, waypoint_repo)
    if shipyard:
        ship_types = list_available_ship_types(agent_repo, waypoint_repo, shipyard)
        print(ship_types)
        for ship_type in ship_types:
            if ship_type == "SHIP_MINING_DRONE":
                buy_ship(agent_repo, waypoint_repo, shipyard, ship_type)
