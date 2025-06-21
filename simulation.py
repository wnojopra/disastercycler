from state import GameState
from victory_checker import check_victory
from yaml_loader import load_characters_from_yaml, load_actions_from_yaml, load_incidents_from_yaml
from engine import check_loss_conditions, resolve_actions, resolve_roles, resolve_incident
from models import Location

def simulate_day_1():
    characters = load_characters_from_yaml("data/characters.yaml")
    incidents = load_incidents_from_yaml("data/incidents.yaml")
    
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
    day1_incident = next((i for i in incidents if i.day == 1), None)
    if day1_incident:
        resolve_incident(game_state, day1_incident)

    print("--- Day 1 State ---")
    game_state.print_characters()

    result = check_victory(game_state)
    if result:
        game_state.game_result = result
        print(f"🏁 Game Over — {result.replace('_', ' ').title()}")
        return

if __name__ == "__main__":
    simulate_day_1()
