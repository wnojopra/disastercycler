import argparse

from engine.models import Location, LocationType

from .engine import (
    reset_for_new_loop,
    resolve_abilities,
    resolve_actions,
    resolve_incident,
    resolve_roles,
)
from .state import GameState
from .victory_checker import check_victory
from .yaml_loader import load_actions_from_yaml, load_script_from_yaml


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
        actions=actions,
    )


def simulate_day(game_state: GameState):
    todays_actions = game_state.actions[game_state.day]
    resolve_actions(game_state, todays_actions)
    resolve_abilities(game_state, todays_actions)
    resolve_roles(game_state)
    resolve_incident(game_state)

    print(f"--- Day {game_state.day} State ---")
    game_state.print_characters()

    check_victory(game_state)
    if game_state.game_result:
        print(f"🏁 Game Over — {game_state.game_result.replace('_', ' ').title()}")
    game_state.day += 1


def run_full_simulation(script_path: str, actions_path: str) -> GameState:
    """
    Runs a full game simulation and returns the final state.
    This function is designed to be testable.
    """
    game_state = create_starting_game_state(script_path, actions_path)

    while game_state.game_result is None:
        if game_state.day > game_state.days_per_loop:
            check_victory(game_state)
            if game_state.game_result is None:
                if game_state.loop_count >= game_state.max_loops:
                    game_state.game_result = "mastermind_win"
                else:
                    reset_for_new_loop(game_state)

        if game_state.game_result is None:
            simulate_day(game_state)

    # After the loop, do one final check on the very last day's state
    check_victory(game_state)
    return game_state


def main():
    parser = argparse.ArgumentParser(description="Run Tragedy Looper simulation.")
    parser.add_argument(
        "script_name", help="Name of the script YAML file (without extension)"
    )
    parser.add_argument(
        "actions_file", help="Name of the actions YAML file (without extension)"
    )

    args = parser.parse_args()

    # Assuming your YAML files live in a folder like 'scripts/' and have a '.yaml' extension
    script_path = f"scripts/{args.script_name}/script.yaml"
    actions_path = f"scripts/{args.script_name}/{args.actions_file}.yaml"

    final_state = run_full_simulation(script_path, actions_path)
    print("\n--- Final Results ---")
    if final_state.game_result:
        print(f"🏁 Game Over — {final_state.game_result.replace('_', ' ').title()}")
    final_state.print_characters()


if __name__ == "__main__":
    main()
