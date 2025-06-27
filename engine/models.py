from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# === ENUMS ===


class RoleType(str, Enum):
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


class LocationType(str, Enum):
    CITY = "city"
    HOSPITAL = "hospital"
    SCHOOL = "school"
    SHRINE = "shrine"


ALL_LOCATIONS = list(LocationType)


class ActionType(str, Enum):
    MOVE_VERTICAL = "move_vertical"
    MOVE_HORIZONTAL = "move_horizontal"
    MOVE_DIAGONAL = "move_diagonal"
    ADD_GOODWILL = "add_goodwill"
    ADD_PARANOIA = "add_paranoia"
    ADD_INTRIGUE = "add_intrigue"


class ActionTargetType(str, Enum):
    CHARACTER = "character"
    LOCATION = "location"


class ActionSource(str, Enum):
    MASTERMIND = "mastermind"
    PROTAGONIST = "protagonist"


class IncidentType(str, Enum):
    MURDER = "murder"
    SUICIDE = "suicide"


# === MODELS ===


class Character(BaseModel):
    name: str
    location: LocationType
    starting_location: LocationType
    disallowed_locations: List[LocationType]
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


class Location(BaseModel):
    location_type: LocationType
    intrigue: int = 0


class Incident(BaseModel):
    type: IncidentType
    day: int
    culprit: str


class Script(BaseModel):
    name: str
    days_per_loop: int
    max_loops: int
    plot: str
    subplots: List[str]
    characters: List[Character]
    incidents: List[Incident]


class Action(BaseModel):
    source: ActionSource
    type: ActionType
    target_type: ActionTargetType
    target: str
    metadata: Dict = Field(default_factory=dict)


class IncidentChoice(BaseModel):
    type: IncidentType
    target: str
    metadata: Dict = Field(default_factory=dict)


class AbilityChoice(BaseModel):
    source: RoleType
    target: str


class TurnData(BaseModel):
    actions: List[Action]
    incident_choices: Optional[List[IncidentChoice]] = None
    ability_actions: Optional[List[AbilityChoice]] = None


AllActionsByDay = Dict[int, TurnData]
