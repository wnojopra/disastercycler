from models import Character, Location
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

def resolve_actions(game_state: GameState, actions: dict[str, dict]):
    for char in game_state.characters:
        if char.name in actions:
            action = actions[char.name]
            if action["type"] == "move":
                resolve_move(char, action["direction"])
            elif action["type"] == "add_paranoia":
                char.paranoia += 1
            elif action["type"] == "add_goodwill":
                char.goodwill += 1


def resolve_roles(game_state: GameState):
    for char in game_state.characters:
        if not char.alive:
            continue
        effect_fn = ROLE_EFFECTS.get(char.role)
        if effect_fn:
            effect_fn(char, game_state)

from models import RoleType
from state import GameState

def check_loss_conditions(game_state: GameState) -> bool:
    """
    Checks if any immediate loss condition is met. Returns True if Protagonists lose.
    """
    for char in game_state.characters:
        if char.role == RoleType.KEY_PERSON and not char.alive:
            print(f"❌ {char.name} (Key Person) died — Protagonists lose immediately!")
            return True

    # TODO: Add other loss conditions like Butterfly Effect, cult victory, etc.
    return False
