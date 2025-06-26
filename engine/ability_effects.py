from .models import Character, RoleType
from .state import GameState

def resolve_conspiracy_theorist_ability(source_char: Character, target_char: Character, game_state: GameState):
    # Find characters at the same location (excluding themself)
    if source_char.location != target_char.location:
        raise ValueError(f"Error resolving conspiracy theorist ability: target at different location")
    else:
        target_char.paranoia += 1

def resolve_brain_ability(source_char: Character, target_char: Character, game_state: GameState):
    if source_char.location != target_char.location:
        raise ValueError(f"Error resolving conspiracy theorist ability: target at different location")
    else:
        target_char.intrigue += 1


# The main registry for all ability logic
ABILITY_LOGIC = {
    RoleType.CONSPIRACY_THEORIST: resolve_conspiracy_theorist_ability,
    RoleType.BRAIN: resolve_brain_ability,
    # Add other roles with abilities here
}