from .models import Character, Location, RoleType
from .state import GameState

def resolve_conspiracy_theorist_ability(source: Character, target: Character | Location):
    assert isinstance(target, Character)
    # Find characters at the same location (excluding themself)
    if source.location != target.location:
        raise ValueError(f"Error resolving conspiracy theorist ability: target at different location")
    else:
        target.paranoia += 1

def resolve_brain_ability(source: Character, target: Character | Location):
    if isinstance(target, Character) and source.location != target.location:
        raise ValueError(f"Error resolving conspiracy theorist ability: target at different location")
    else:
        target.intrigue += 1


# The main registry for all ability logic
ABILITY_LOGIC = {
    RoleType.CONSPIRACY_THEORIST: resolve_conspiracy_theorist_ability,
    RoleType.BRAIN: resolve_brain_ability,
    # Add other roles with abilities here
}