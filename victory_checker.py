from state import GameState
from models import RoleType

def check_victory(game_state: GameState) -> str | None:
    """
    Determines win/loss outcome. Returns:
    - "mastermind_win"
    - "protagonists_win"
    - None (if game continues)
    """
    # Key Person dies → Mastermind wins instantly
    for char in game_state.characters:
        if char.role == RoleType.KEY_PERSON and not char.alive:
            print(f"❌ {char.name} (Key Person) is dead — Mastermind wins!")
            return "mastermind_win"

    # Future: Butterfly Effect
    # if game_state.butterfly_effect_triggered:
    #     print("🦋 Butterfly Effect triggered — Mastermind wins!")
    #     return "mastermind_win"

    # Future: all loops used & tragedy prevented
    #
