import yaml
from .models import Action, ActionSource, ActionTargetType, ActionType, AllActionsByDay, Character, IncidentChoice, IncidentType, Location, RoleType, Incident, Script, TurnData

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
    if "incidents" in data:
        for entry in data["incidents"]:
            incident = Incident(
                type = IncidentType[entry["type"]],
                day = entry["day"],
                culprit = entry["culprit"]
            )
            incidents.append(incident)

    return Script(
        name=data["name"],
        days_per_loop=data["days_per_loop"],
        max_loops=data["max_loops"],
        plot=data["plot"],
        subplots=data["subplots"],
        characters=characters,
        incidents=incidents
    )


def load_actions_from_yaml(file_path: str) -> AllActionsByDay:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    actions_by_day: AllActionsByDay = {}

    def parse_actions(source: ActionSource, actions_raw: list, day: int) -> list[Action]:
        parsed = []
        for i, action_dict in enumerate(actions_raw):
            if "type" not in action_dict or "target" not in action_dict:
                raise ValueError(f"Missing 'type' or 'target' in {source} action on day {day}, index {i}")

            target_str = action_dict["target"]
            # Infer target_type based on name
            if target_str.lower() in {loc.value for loc in Location}:
                target_type = ActionTargetType.LOCATION
            else:
                target_type = ActionTargetType.CHARACTER


            try:
                action_type = ActionType[action_dict["type"]]
            except ValueError as e:
                raise ValueError(f"Invalid enum value in {source} action on day {day}, index {i}: {e}")

            metadata = action_dict.get("metadata", {})
            parsed.append(Action(
                source=source,
                type=action_type,
                target_type=target_type,
                target=action_dict["target"],
                metadata=metadata
            ))
        return parsed

    def parse_incident_choices(choices_raw: list, day: int) -> list[IncidentChoice]:
        parsed = []
        for i, c in enumerate(choices_raw):
            if "incident_type" not in c or "target" not in c:
                raise ValueError(f"Missing 'incident_type' or 'target' in incident_choice on day {day}, index {i}")
            try:
                incident_type = IncidentType[c["incident_type"]]
            except ValueError:
                raise ValueError(f"Invalid incident_type '{c['incident_type']}' on day {day}, index {i}")
            parsed.append(IncidentChoice(
                type=incident_type,
                target=c["target"],
                metadata=c.get("metadata", {})
            ))
        return parsed

    for entry in data:
        day = entry.get("day")
        if day is None:
            raise ValueError("Each entry must include a 'day' field.")

        all_actions: list[Action] = []

        for role_str in ["mastermind", "protagonist"]:
            if role_str not in entry:
                raise ValueError(f"Day {day} must include '{role_str}' actions.")

            role_enum = ActionSource(role_str)
            all_actions.extend(parse_actions(role_enum, entry[role_str], day))

        incident_choices = None
        if "incident_choices" in entry:
            incident_choices = parse_incident_choices(entry["incident_choices"], day)

        actions_by_day[day] = TurnData(
            actions=all_actions,
            incident_choices=incident_choices
        )

    return actions_by_day

