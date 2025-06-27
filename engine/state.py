from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .models import (
    AllActionsByDay,
    Character,
    Incident,
    Location,
    LocationType,
    RoleType,
)


@dataclass
class GameState:
    day: int
    loop_count: int
    days_per_loop: int
    max_loops: int
    characters: List[Character]
    incidents: List[Incident]
    actions: AllActionsByDay
    location_states: Dict[LocationType, Location] = field(
        default_factory=lambda: {
            location_type: Location(location_type=location_type)
            for location_type in LocationType
        }
    )
    game_result: Optional[str] = None  # "protagonists_win", "mastermind_win", or None
    revealed_roles: Set[RoleType] = field(default_factory=set)

    def print_characters(self):
        for char in self.characters:
            message = f"{char.name} is at {char.location.name}, paranoia={char.paranoia}, goodwill={char.goodwill}, intrigue={char.intrigue}"
            if not char.alive:
                message += ", status=DEAD"
            print(message)
