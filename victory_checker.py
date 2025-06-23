from state import GameState
from models import RoleType

def check_victory(game_state: GameState):
    """
    Determines win/loss outcome and updates game_state.game_result
    """
    # Key Person dies → Mastermind wins instantly
    for char in game_state.characters:
        if char.role == RoleType.KEY_PERSON and not char.alive:
            print(f"❌ {char.name} (Key Person) is dead — Mastermind wins!")
            game_state.game_result = "mastermind_win"
            return
    # Future: Butterfly Effect
    # if game_state.butterfly_effect_triggered:
    #     print("🦋 Butterfly Effect triggered — Mastermind wins!")
    #     return "mastermind_win"

    # Future: all loops used & tragedy prevented
    #
