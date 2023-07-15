from typing import Optional

from src.domain.model import AgentRepository, Waypoint, WaypointRepository


def find_local_shipyard(agent_repo: AgentRepository,
                        waypoint_repo: WaypointRepository) -> Optional[Waypoint]:
    agent = agent_repo.get_agent()
    home_system = "-".join(agent.headquarters.waypoint.split("-")[0:2])
    waypoints = waypoint_repo.get_waypoints_in_system(home_system, agent.token)

    for wp in waypoints:
        if "SHIPYARD" in wp.traits:
            return wp
    return None


# 2. Purchase a ship
# 2.a. List all available ship types in a shipyard
# 2.b Buy the right ship from the shipyard (or raise a Domain exception if we don't have enough money)
# ==> Can be done with constants for now, no need for complex logic
