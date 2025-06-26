from engine.simulation import run_full_simulation
from engine.models import RoleType

def test_friend_dies_at_end_of_loop():
    """
    Tests the scenario where the Friend dies on the last day,
    resulting in a win for the Mastermind.
    """
    # 1. Arrange: Define the input files for this specific scenario
    script_path = "scripts/testing_roles/script.yaml"
    actions_path = "scripts/testing_roles/actions_fd.yaml" # You create this file
    
    # 2. Act: Run the simulation and get the final state
    final_state = run_full_simulation(script_path, actions_path)
    
    # 3. Assert: Automatically check if the outcome is what we expect
    assert final_state.game_result == "mastermind_win"
    
    # You can add more specific assertions too!
    friend_char = next(c for c in final_state.characters if c.role == RoleType.FRIEND)
    assert not friend_char.alive
    assert RoleType.FRIEND in final_state.revealed_roles

def test_serial_killer_gets_key_person():
    script_path = "scripts/the_first_script/script.yaml"
    actions_path = "scripts/the_first_script/actions_1.yaml"
    final_state = run_full_simulation(script_path, actions_path)
    assert final_state.game_result == "mastermind_win"
    key_person = next(c for c in final_state.characters if c.role == RoleType.KEY_PERSON)
    assert not key_person.alive

def test_key_person_murdered():
    script_path = "scripts/the_first_script/script.yaml"
    actions_path = "scripts/the_first_script/actions_2.yaml"
    final_state = run_full_simulation(script_path, actions_path)
    assert final_state.game_result == "mastermind_win"
    key_person = next(c for c in final_state.characters if c.role == RoleType.KEY_PERSON)
    assert not key_person.alive

def test_key_person_suicides():
    script_path = "scripts/the_first_script/script.yaml"
    actions_path = "scripts/the_first_script/actions_3.yaml"
    final_state = run_full_simulation(script_path, actions_path)
    assert final_state.game_result == "mastermind_win"
    key_person = next(c for c in final_state.characters if c.role == RoleType.KEY_PERSON)
    assert not key_person.alive

def test_protagonists_win():
    script_path = "scripts/the_first_script/script.yaml"
    actions_path = "scripts/the_first_script/actions_4.yaml"
    final_state = run_full_simulation(script_path, actions_path)
    assert final_state.game_result == "protagonist_win"
    assert all(char.alive for char in final_state.characters)

def test_conspiracy_theorist_ability():
    script_path = "scripts/the_first_script/script.yaml"
    actions_path = "scripts/the_first_script/actions_ct.yaml"
    final_state = run_full_simulation(script_path, actions_path)
    assert final_state.game_result == "mastermind_win"
    key_person = next(c for c in final_state.characters if c.role == RoleType.KEY_PERSON)
    assert not key_person.alive