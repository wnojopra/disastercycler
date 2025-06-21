import yaml
from typing import Dict, List, Union
from models import Character, Location, RoleType, Incident

def load_characters_from_yaml(path: str) -> List[Character]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    characters = []
    for entry in data["characters"]:
        character = Character(
            name=entry["name"],
            location=Location[entry["location"]],
            starting_location=Location[entry["starting_location"]],
            disallowed_locations=[Location[loc] for loc in entry["disallowed_locations"]],
            role=RoleType[entry["role"]]
        )
        characters.append(character)

    return characters


def load_actions_from_yaml(path: str) -> Dict[str, Dict[str, Union[str, Location]]]:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    actions = {}
    for entry in raw["actions"]:
        char_name = entry["character"]
        action_type = entry["type"]
        action = {"type": action_type}
        if action_type == "move":
            action["direction"] = entry["direction"]
        actions[char_name] = action

    return actions

def load_incidents_from_yaml(path: str) -> List[Incident]:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
   
    incidents = []
    for entry in raw["incidents"]:
        incident = Incident(
            name = entry["name"],
            day = entry["day"],
            culprit = entry["culprit"]
        )
        incidents.append(incident)

    return incidents