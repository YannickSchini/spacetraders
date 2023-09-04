from typing import Dict, List, Optional, Set

import requests as req
import structlog
from requests.models import HTTPError

from src.domain.waypoint import System, SystemRepository, Waypoint

logger = structlog.get_logger()


class HttpSystemRepository(SystemRepository):
    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> System:

        logger.info(f"Getting the waypoints in system {target_system}")
        response = req.get(
            url = f"https://api.spacetraders.io/v2/systems/{target_system}/waypoints",
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        waypoints: List[Waypoint] = []
        for raw_waypoint in response.json()["data"]:
            traits: List[str] = []
            for raw_trait in raw_waypoint["traits"]:
                traits.append(raw_trait["symbol"])
            waypoints.append(Waypoint(waypoint=raw_waypoint["symbol"], traits=traits))

        return System(set(waypoints))

    def list_available_ship_types(self,
                                  shipyard: Waypoint,
                                  agent_token: str) -> Set[str]:
        logger.info(f"Getting the available ship types in shipyard {shipyard}")
        system = "-".join(shipyard.waypoint.split("-")[0:2])
        response = req.get(
            url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{shipyard.waypoint}/shipyard", # noqa
            headers = {"Authorization": f"Bearer {agent_token}"}
        )
        if response.status_code > 299:
            raise HTTPError(response.text)
        ship_types: Set[str] = set()
        for ship in response.json()["data"]["ships"]:
            ship_types.add(ship["type"])

        return ship_types

    def buy_ship(self,
                 shipyard: Waypoint,
                 agent_token: str,
                 ship_type: str) -> None:

        data = {"shipType": ship_type, "waypointSymbol": shipyard.waypoint}
        logger.info(f"Buying a {ship_type} ship at shipyard {shipyard}")
        response = req.post(
            url = "https://api.spacetraders.io/v2/my/ships",
            headers = {
                "Authorization": f"Bearer {agent_token}",
                "Content-Type": "application/json"
            },
            json = data,
        )
        if response.status_code > 299:
            raise HTTPError(response.text)

class InMemorySystemRepository(SystemRepository):
    def __init__(self,
                 systems: Optional[Dict[str, List[Waypoint]]] = None,
                 shipyards: Optional[Dict[Waypoint, Set[str]]] = None) -> None:
        if systems is None:
            self.systems = {}
        else:
            self.systems = systems
        if shipyards is None:
            self.shipyards = {}
        else:
            self.shipyards = shipyards

    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> System:
        logger.info(f"Getting the waypoints in system {target_system}")
        return System(set(self.systems[target_system]))

    def list_available_ship_types(self,
                                  shipyard: Waypoint,
                                  agent_token: str) -> Set[str]:
        logger.info(f"Getting the available ship types in shipyard {shipyard}")
        return self.shipyards[shipyard]

    def buy_ship(self,
                 shipyard: Waypoint,
                 agent_token: str,
                 ship_type: str) -> None:
        pass

    def add_waypoint(self,
                     waypoint_id: str = "X1-YY2-XXXX5",
                     traits: Optional[List[str]] = None) -> None:
        if traits is None:
            traits = ["COLD", "SMALL", "EMPTY"]
        system_id = "-".join(waypoint_id.split("-")[0:2])
        if system_id in self.systems:
            self.systems[system_id].append(
                Waypoint(waypoint=waypoint_id, traits=traits)
            )
        else:
            self.systems[system_id] = [Waypoint(waypoint=waypoint_id, traits=traits)]


    def add_shipyard(
        self,
        shipyard_id: str = "A1-BB2-XXXX5",
        ship_list: Optional[Set[str]] = None,
    ) -> None:
        if ship_list is None:
            ship_list = {"BIG_SHIP", "SMALL_SHIP", "SMALLEST_SHIP"}
        shipyard_wp = Waypoint(waypoint=shipyard_id)
        self.shipyards[shipyard_wp] = ship_list

