from .models import Character, RoleType
from .state import GameState

def resolve_conspiracy_theorist_ability(source_char: Character, target_char: Character, game_state: GameState):
    """
    The Conspiracy Theorist can use ADD_PARANOIA on anyone at their location.
    """
    # Find characters at the same location (excluding themself)
    if source_char.location != target_char.location:
        raise ValueError(f"Error resolving conspiracy theorist ability: target at different location")
    else:
        target_char.paranoia += 1

# The main registry for all ability logic
ABILITY_LOGIC = {
    RoleType.CONSPIRACY_THEORIST: resolve_conspiracy_theorist_ability,
    # Add other roles with abilities here
}