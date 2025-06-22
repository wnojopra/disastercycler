from state import GameState
from victory_checker import check_victory
from yaml_loader import load_actions_from_yaml, load_script_from_yaml
from engine import resolve_actions, resolve_roles, resolve_incident
from models import Location

def simulate_day_1() -> GameState:
    script = load_script_from_yaml("scripts/the_first_script.yaml")
    characters = script.characters
    incidents = script.incidents
    actions = load_actions_from_yaml("data/actions_day1.yaml")
    
    game_state = GameState(
        day=1,
        loop_count=1,
        max_loops=3,
        characters=characters,
        incidents=incidents
    )

    resolve_actions(game_state, actions)
    resolve_roles(game_state)
    resolve_incident(game_state)

    print("--- Day 1 State ---")
    game_state.print_characters()

    result = check_victory(game_state)
    if result:
        game_state.game_result = result
        print(f"🏁 Game Over — {result.replace('_', ' ').title()}")
    return game_state
    
def simulate_day_2(game_state: GameState) -> GameState:
    game_state.day = 2
    actions = load_actions_from_yaml("data/actions_day2.yaml")
    resolve_actions(game_state, actions)
    resolve_roles(game_state)
    resolve_incident(game_state)

    print("--- Day 2 State ---")
    game_state.print_characters()

    result = check_victory(game_state)
    if result:
        game_state.game_result = result
        print(f"🏁 Game Over — {result.replace('_', ' ').title()}")
    return game_state

if __name__ == "__main__":
    game_state = simulate_day_1()
    simulate_day_2(game_state)
