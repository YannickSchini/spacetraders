from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class Waypoint():
    waypoint: str
    traits: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Waypoint {self.waypoint} with traits {self.traits}"

    def __hash__(self) -> int:
        return hash((self.waypoint, "".join(sorted(self.traits))))


@dataclass
class System:
    waypoints: Set[Waypoint]

    def __repr__(self) -> str:
        system_prefix = next(iter(self.waypoints)).waypoint.split("-")[0:1]
        return f"System {system_prefix}"

class SystemRepository(ABC):
    @abstractmethod
    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> System:
        raise NotImplementedError

    @abstractmethod
    def list_available_ship_types(self,
                                  shipyard: Waypoint,
                                  agent_token: str) -> Set[str]:
        raise NotImplementedError

    @abstractmethod
    def buy_ship(self,
                 shipyard: Waypoint,
                 agent_token: str,
                 ship_type: str) -> None:
        raise NotImplementedError
