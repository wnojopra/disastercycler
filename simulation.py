import argparse
from state import GameState
from victory_checker import check_victory
from yaml_loader import load_actions_from_yaml, load_script_from_yaml
from engine import resolve_actions, resolve_roles, resolve_incident

def create_starting_game_state(script_path: str, actions_path: str) -> GameState:
    day = 1
    script = load_script_from_yaml(script_path)
    actions = load_actions_from_yaml(actions_path)
    
    return GameState(
        day=day,
        loop_count=1,
        days_per_loop=script.days_per_loop,
        max_loops=script.max_loops,
        characters=script.characters,
        incidents=script.incidents,
        actions=actions
    )

def simulate_day(game_state: GameState):
    todays_actions = game_state.actions[game_state.day]
    resolve_actions(game_state, todays_actions)
    resolve_roles(game_state)
    resolve_incident(game_state)

    print(f"--- Day {game_state.day} State ---")
    game_state.print_characters()

    check_victory(game_state)
    if game_state.game_result:
        print(f"🏁 Game Over — {game_state.game_result.replace('_', ' ').title()}")
    game_state.day += 1

def main():
    parser = argparse.ArgumentParser(description="Run Tragedy Looper simulation.")
    parser.add_argument("script_name", help="Name of the script YAML file (without extension)")
    parser.add_argument("actions_file", help="Name of the actions YAML file (without extension)")

    args = parser.parse_args()

    # Assuming your YAML files live in a folder like 'scripts/' and have a '.yaml' extension
    script_path = f"scripts/{args.script_name}/script.yaml"
    actions_path = f"scripts/{args.script_name}/{args.actions_file}.yaml"

    game_state = create_starting_game_state(script_path, actions_path)
    while game_state.game_result is None:
        simulate_day(game_state)


if __name__ == "__main__":
    main()

