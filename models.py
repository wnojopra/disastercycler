from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, TypeAlias


class RoleType(Enum):
    BRAIN = "brain"
    CONSPIRACY_THEORIST = "conspiracy_theorist"
    CULTIST = "cultist"
    FRIEND = "friend"
    KEY_PERSON = "key_person"
    KILLER = "killer"
    LOVED_ONE = "loved_one"
    LOVER = "lover"
    PERSON = "person"
    SERIAL_KILLER = "serial_killer"
    TIME_TRAVELLER = "time_traveller"
    WITCH = "witch"

class Location(Enum):
    CITY = "city"
    HOSPITAL = "hospital"
    SCHOOL = "school"
    SHRINE = "shrine"

ALL_LOCATIONS = list(Location)

class ActionType(Enum):
    MOVE_VERTICAL = "move_vertical"
    MOVE_HORIZONTAL = "move_horizontal"
    MOVE_DIAGONAL = "move_diagonal"
    ADD_GOODWILL = "add_goodwill"
    ADD_PARANOIA = "add_paranoia"

@dataclass
class Character:
    name: str
    location: Location
    starting_location: Location
    disallowed_locations: List[Location]
    paranoia: int = 0
    paranoia_limit: int = 0
    goodwill: int = 0
    intrigue: int = 0
    role: RoleType = RoleType.PERSON
    alive: bool = True

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return NotImplemented
        return self.name == other.name

class IncidentType(Enum):
    MURDER = "murder"
    SUICIDE = "suicide"

@dataclass
class Incident:
    type: IncidentType
    day: int
    culprit: str

@dataclass
class Script:
    name: str
    days_per_loop: int
    max_loops: int
    plot: str
    subplots: List[str]

    characters: List[Character]
    incidents: List[Incident]

@dataclass
class Action:
    type: ActionType | IncidentType
    target: str

AllActionsByDay: TypeAlias = Dict[int, Dict[str, List[Action]]]
