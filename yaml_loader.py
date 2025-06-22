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
        each mapping to a list of Action instances.
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    actions_by_day: Dict[int, Dict[str, List[Action]]] = {}

    def parse_actions(role: str, actions_raw: List[dict], day: int) -> List[Action]:
        parsed = []
        for i, action_dict in enumerate(actions_raw):
            if "type" not in action_dict or "target" not in action_dict:
                raise ValueError(f"Missing 'type' or 'target' in {role} action on day {day}, index {i}")
            try:
                action_type = ActionType[action_dict["type"]]
            except KeyError:
                raise ValueError(f"Invalid action type '{action_dict['type']}' for {role} on day {day}, index {i}")
            parsed.append(Action(type=action_type, target=action_dict["target"]))
        return parsed

    for entry in data:
        day = entry.get("day")
        if day is None:
            raise ValueError("Each entry must include a 'day' field.")

        for role in ["mastermind", "protagonist"]:
            if role not in entry:
                raise ValueError(f"Day {day} must include '{role}' actions.")

        actions_by_day[day] = {
            role: parse_actions(role, entry[role], day)
            for role in ["mastermind", "protagonist"]
        }

    return actions_by_day

