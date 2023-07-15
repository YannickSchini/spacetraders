from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class Waypoint():
    waypoint: str
    traits: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Waypoint {self.waypoint} with traits {self.traits}"

class WaypointRepository(ABC):
    @abstractmethod
    def get_waypoints_in_system(self,
                                target_system: str,
                                agent_token: str) -> List[Waypoint]:
        raise NotImplementedError
