from state import GameState
from victory_checker import check_victory
from yaml_loader import load_actions_from_yaml, load_script_from_yaml
from engine import resolve_actions, resolve_roles, resolve_incident
from models import Location

def simulate_day_1() -> GameState:
    day = 1
    script = load_script_from_yaml("scripts/the_first_script/script.yaml")
    all_actions = load_actions_from_yaml("scripts/the_first_script/actions_1.yaml")
    todays_actions = all_actions[day]
    
    game_state = GameState(
        day=day,
        loop_count=1,
        max_loops=script.max_loops,
        characters=script.characters,
        incidents=script.incidents
    )

    resolve_actions(game_state, todays_actions)
    resolve_roles(game_state)
    resolve_incident(game_state)

    print(f"--- Day {day} State ---")
    game_state.print_characters()

    result = check_victory(game_state)
    if result:
        game_state.game_result = result
        print(f"🏁 Game Over — {result.replace('_', ' ').title()}")
    return game_state

if __name__ == "__main__":
    game_state = simulate_day_1()
