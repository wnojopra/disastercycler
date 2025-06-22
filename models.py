from dataclasses import dataclass
from enum import Enum
from typing import List


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

@dataclass
class Incident:
    name: str
    day: int
    culprit: Character