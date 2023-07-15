from typing import Dict, List

import requests as req

from src.domain.model import Waypoint, WaypointRepository


class HttpWaypointRepository(WaypointRepository):
    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> List[Waypoint]:
        
        response = req.get(
            url = f"https://api.spacetraders.io/v2/systems/{target_system}/waypoints",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        waypoints = []
        for raw_waypoint in response.json()["data"]:
            traits = []
            for raw_trait in raw_waypoint["traits"]:
                traits.append(raw_trait["symbol"])
            waypoints.append(Waypoint(waypoint=raw_waypoint["symbol"], traits=traits))

        return waypoints

class InMemoryWaypoinyRepository(WaypointRepository):
    def __init__(self, waypoints: Dict[str, List[Waypoint]]) -> None:
        self.waypoints = waypoints

    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> List[Waypoint]:
        return self.waypoints[target_system]
