from collections import defaultdict
from typing import Dict, List

from engine.ability_effects import ABILITY_LOGIC

from .incident_effects import INCIDENT_EFFECTS
from .models import (
    ALL_LOCATIONS,
    Action,
    ActionType,
    Character,
    LocationType,
    RoleType,
    TurnData,
)
from .role_effects import ROLE_EFFECTS
from .state import GameState

# Define the layout as a 2x2 grid
LOCATION_GRID = [
    [LocationType.HOSPITAL, LocationType.SHRINE],  # Top row
    [LocationType.CITY, LocationType.SCHOOL],  # Bottom row
]


def find_location_coords(location: LocationType) -> tuple[int, int]:
    for row_idx, row in enumerate(LOCATION_GRID):
        for col_idx, loc in enumerate(row):
            if loc == location:
                return row_idx, col_idx
    raise ValueError(f"Unknown location: {location}")


def resolve_move(char: Character, action_type: ActionType):
    """
    Moves a character based on spatial direction if the destination is not disallowed.
    action_type is one of: "VERTICAL", "HORIZONTAL", "DIAGONAL".
    """
    row, col = find_location_coords(char.location)

    candidates = []
    if action_type == ActionType.MOVE_VERTICAL:
        new_row = 1 - row
        candidates.append(LOCATION_GRID[new_row][col])
    elif action_type == ActionType.MOVE_HORIZONTAL:
        new_col = 1 - col
        candidates.append(LOCATION_GRID[row][new_col])
    elif action_type == ActionType.MOVE_DIAGONAL:
        new_row = 1 - row
        new_col = 1 - col
        candidates.append(LOCATION_GRID[new_row][new_col])
    else:
        raise ValueError(f"Invalid direction: {action_type}")

    for loc in candidates:
        if loc not in char.disallowed_locations:
            char.location = loc
            return

    # If no valid move
    print(f"{char.name} could not move due to disallowed location restriction.")


def resolve_action(char: Character, action_type: ActionType):
    if action_type in [
        ActionType.MOVE_DIAGONAL,
        ActionType.MOVE_HORIZONTAL,
        ActionType.MOVE_VERTICAL,
    ]:
        resolve_move(char, action_type)
    elif action_type == ActionType.ADD_PARANOIA:
        char.paranoia += 1
    elif action_type == ActionType.ADD_GOODWILL:
        char.goodwill += 1
    elif action_type == ActionType.ADD_INTRIGUE:
        char.intrigue += 1
    else:
        raise ValueError(f"Invalid action type {action_type}")


def resolve_actions(game_state: GameState, turn_data: TurnData):
    # Group actions by target
    char_to_actions: Dict[Character, List[Action]] = defaultdict(list)
    loc_to_actions: Dict[str, List[Action]] = defaultdict(list)

    for action in turn_data.actions:
        if action.target in ALL_LOCATIONS:
            loc_to_actions[action.target].append(action)
        else:
            char = next(
                (c for c in game_state.characters if c.name == action.target), None
            )
            if not char:
                raise ValueError(f"Unknown character target: {action.target}")
            char_to_actions[char].append(action)

    # Resolve actions targeting characters
    for char, action_list in char_to_actions.items():
        for action in action_list:
            resolve_action(char, action.type)

    # TODO: Resolve location-based actions (not yet implemented)
    # for loc, action_list in loc_to_actions.items():
    #     ...


def resolve_abilities(game_state: GameState, turn_data: TurnData):
    """
    Resolves the ability actions chosen by players for the turn.
    """
    if not turn_data.ability_actions:
        return  # Skip if no abilities were used

    print("--- 🎭 Abilities Phase ---")

    for choice in turn_data.ability_actions:
        source_char = next(
            (c for c in game_state.characters if c.role == choice.source), None
        )
        if choice.target.lower() in {l.value for l in LocationType}:
            target_loc_enum = LocationType(choice.target.lower())
            target_obj = game_state.location_states[target_loc_enum]
        else:
            target_obj = next(
                (c for c in game_state.characters if c.name == choice.target), None
            )

        if not source_char or not target_obj:
            print(
                f"Warning: Invalid character or location in ability choice, skipping."
            )
            continue

        ability_fn = ABILITY_LOGIC.get(source_char.role)
        if not ability_fn:
            print(
                f"Warning: {source_char.name} ({source_char.role.name}) has no defined ability, skipping."
            )
            continue

        ability_fn(source_char, target_obj)


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
            print(f"🔴 The {incident.type} incident happens on day {game_state.day}")
            effect_fn = INCIDENT_EFFECTS.get(incident.type)
            if effect_fn:
                effect_fn(culprit, incident, game_state)
        else:
            print(
                f"🟢 The {incident.type} incident does not happen on day {game_state.day}"
            )


def reset_for_new_loop(game_state: GameState):
    """Resets the game state for the start of a new loop."""
    print("--- 🔁 STARTING NEW LOOP ---")
    game_state.loop_count += 1
    game_state.day = 1

    # Reset each character to their starting state
    for char in game_state.characters:
        char.location = char.starting_location
        char.paranoia = 0
        char.goodwill = 0  # Reset goodwill to 0 first for everyone
        char.intrigue = 0
        char.alive = True

    # Now, apply the Friend's special bonus
    if RoleType.FRIEND in game_state.revealed_roles:
        try:
            friend_char = next(
                c for c in game_state.characters if c.role == RoleType.FRIEND
            )
            friend_char.goodwill = 1
            print(
                f"✨ The Friend ({friend_char.name}) has been revealed and starts with 1 Goodwill."
            )
        except StopIteration:
            pass  # No friend in script
