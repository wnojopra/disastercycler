from .models import RoleType
from .state import GameState


def check_friend_loss_condition(game_state: GameState):
    """
    Checks if the Friend is dead at the end of the loop.
    If so, the Mastermind wins and the Friend role is revealed.
    """
    # This rule only applies on the last day of a loop
    if game_state.day != game_state.days_per_loop:
        return

    try:
        friend_char = next(
            c for c in game_state.characters if c.role == RoleType.FRIEND
        )

        if not friend_char.alive:
            print(f"💔 The Friend ({friend_char.name}) is dead at the end of the loop!")
            game_state.game_result = "mastermind_win"
            game_state.revealed_roles.add(RoleType.FRIEND)

    except StopIteration:
        # No Friend character in this script, so we do nothing.
        return


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

    check_friend_loss_condition(game_state)

    if game_state.game_result is None and (game_state.day == game_state.days_per_loop):
        print(
            f"🏆 The end of the last day has ended with no tragedies. Protagonists win!"
        )
        game_state.game_result = "protagonist_win"
        return
