from models import Character, RoleType
from state import GameState

def resolve_serial_killer(char: Character, game_state: GameState):
    if not char.alive:
        return

    others = [
        c for c in game_state.characters
        if c.alive and c.location == char.location and c != char
    ]
    if len(others) == 1:
        victim = others[0]
        victim.alive = False
        print(f"💀 {char.name} (Serial Killer) killed {victim.name} at {char.location.name}")

# Placeholder for other roles
def resolve_cultist(char: Character, game_state: GameState):
    pass

def resolve_friend(char: Character, game_state: GameState):
    pass

ROLE_EFFECTS = {
    RoleType.SERIAL_KILLER: resolve_serial_killer,
    RoleType.CULTIST: resolve_cultist,
    RoleType.FRIEND: resolve_friend,
    # Add others as needed
}
