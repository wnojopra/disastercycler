import yaml
from typing import Any, Dict, List, Union
from models import Action, ActionType, Character, Location, RoleType, Incident, Script

def load_script_from_yaml(path: str) -> Script:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    characters = []
    for entry in data["characters"]:
        character = Character(
            name=entry["name"],
            location=Location[entry["starting_location"]],
            starting_location=Location[entry["starting_location"]],
            disallowed_locations=[Location[loc] for loc in entry["disallowed_locations"]],
            paranoia_limit=entry["paranoia_limit"],
            role=RoleType[entry["role"]]
        )
        characters.append(character)

    incidents = []
    for entry in data["incidents"]:
        incident = Incident(
            name = entry["name"],
            day = entry["day"],
            culprit = entry["culprit"]
        )
        incidents.append(incident)

    return Script(
        name=data["name"],
        days_per_loop=data["days_per_loop"],
        max_loops=data["max_loops"],
        characters=characters,
        incidents=incidents
    )

def load_actions_from_yaml(file_path: str) -> Dict[int, Dict[str, List[Action]]]:
    """
    Load and validate a sequence of actions for each day from a YAML file.
    
    Returns:
        A dict with day as the key and value as another dict with keys 'mastermind' and 'protagonist',
        each mapping to a list of actions.
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    actions_by_day: Dict[int, Dict[str, List[Action]]] = {}

    for entry in data:
        day = entry.get("day")
        if day is None:
            raise ValueError("Each entry must include a 'day' field.")

        if "mastermind" not in entry or "protagonist" not in entry:
            raise ValueError(f"Day {day} must include both 'mastermind' and 'protagonist' actions.")
        
        actions_by_day[day] = {}

        actions: List[Action] = []
        for a in entry["mastermind"]:
            actions.append(Action(type=ActionType[a["type"]], target=a["target"]))
            actions_by_day[day]["mastermind"] = actions
        actions = []
        for a in entry["protagonist"]:
            actions.append(Action(type=ActionType[a["type"]], target=a["target"]))
            actions_by_day[day]["protagonist"] = actions
    return actions_by_day
