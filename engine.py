from typing import Dict, List
from models import Action, Character, Location, ActionType, ALL_LOCATIONS
from role_effects import ROLE_EFFECTS
from state import GameState

# Define the layout as a 2x2 grid
LOCATION_GRID = [
    [Location.HOSPITAL, Location.SHRINE],   # Top row
    [Location.CITY, Location.SCHOOL]        # Bottom row
]

def find_location_coords(location: Location) -> tuple[int, int]:
    for row_idx, row in enumerate(LOCATION_GRID):
        for col_idx, loc in enumerate(row):
            if loc == location:
                return row_idx, col_idx
    raise ValueError(f"Unknown location: {location}")

def resolve_move(char: Character, direction: str):
    """
    Moves a character based on spatial direction if the destination is not disallowed.
    Direction is one of: "VERTICAL", "HORIZONTAL", "DIAGONAL".
    """
    row, col = find_location_coords(char.location)

    candidates = []
    if direction == "VERTICAL":
        new_row = 1 - row
        candidates.append(LOCATION_GRID[new_row][col])
    elif direction == "HORIZONTAL":
        new_col = 1 - col
        candidates.append(LOCATION_GRID[row][new_col])
    elif direction == "DIAGONAL":
        new_row = 1 - row
        new_col = 1 - col
        candidates.append(LOCATION_GRID[new_row][new_col])
    else:
        raise ValueError(f"Invalid direction: {direction}")

    for loc in candidates:
        if loc not in char.disallowed_locations:
            char.location = loc
            return

    # If no valid move
    print(f"{char.name} could not move due to disallowed location restriction.")

def resolve_action(char: Character, action_type: ActionType):
    if action_type == ActionType.MOVE_VERTICAL:
        print(f"here,{action_type}")
        resolve_move(char, "VERTICAL")
    elif action_type == ActionType.ADD_PARANOIA:
        char.paranoia += 1
    elif action_type == ActionType.ADD_GOODWILL:
        char.goodwill += 1
    else:
        raise ValueError(f"Invalid action type {action_type}")

def resolve_actions(game_state: GameState, actions: Dict[str, List[Action]]):
    # First, create a dict keyed by each target with an action, value is a list of its actions
    char_to_actions: Dict[Character, List[Action]] = {}
    loc_to_actions = {}
    for action in actions["mastermind"] + actions["protagonist"]:
        if action.target in ALL_LOCATIONS:
            if action.target not in loc_to_actions:
                loc_to_actions[action.target] = [action]
            else:
                loc_to_actions[action.target].append(action)
        else:
            char = next(c for c in game_state.characters if c.name == action.target)
            if char not in char_to_actions:
                char_to_actions[char] = [action]
            else:
                char_to_actions[char].append(action)
    # Now for each character, resolve each action
    # Later on we need to handle resolving pairs of actions
    for char in char_to_actions:
        for action in char_to_actions[char]:
            resolve_action(char, action.type)

def resolve_roles(game_state: GameState):
    for char in game_state.characters:
        if not char.alive:
            continue
        effect_fn = ROLE_EFFECTS.get(char.role)
        if effect_fn:
            effect_fn(char, game_state)

def resolve_incident(game_state: GameState):
    incident = next((i for i in game_state.incidents if i.day == game_state.day), None)
    if incident is None:
        print(f"🟢 No incident on day {game_state.day}")
    else:
        culprit = next(c for c in game_state.characters if c.name == incident.culprit)
        if culprit.paranoia >= culprit.paranoia_limit:
            print(f"🔴 The {incident.name} incident happens on day {game_state.day}")
