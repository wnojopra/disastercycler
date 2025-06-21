from state import GameState
from victory_checker import check_victory
from yaml_loader import load_characters_from_yaml, load_actions_from_yaml
from engine import check_loss_conditions, resolve_actions, resolve_roles
from models import Location

def simulate_day_1():
    characters = load_characters_from_yaml("data/characters.yaml")
    
    game_state = GameState(
        day=1,
        loop_count=1,
        max_loops=3,
        characters=characters,
        incidents=[]
    )

    actions = load_actions_from_yaml("data/actions_day1.yaml")

    resolve_actions(game_state, actions)
    resolve_roles(game_state)

    print("--- Day 1 State ---")
    game_state.print_characters()

    result = check_victory(game_state)
    if result:
        game_state.game_result = result
        print(f"🏁 Game Over — {result.replace('_', ' ').title()}")
        return

if __name__ == "__main__":
    simulate_day_1()
