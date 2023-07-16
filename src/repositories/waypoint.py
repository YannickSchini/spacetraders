from typing import Dict, List

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.waypoint import Waypoint, WaypointRepository

logger = structlog.get_logger()


class HttpWaypointRepository(WaypointRepository):
    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> List[Waypoint]:
        
        logger.info(f"Getting the waypoints in system {target_system}")
        response = req.get(
            url = f"https://api.spacetraders.io/v2/systems/{target_system}/waypoints",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
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
