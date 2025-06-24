from .models import Character, Incident, IncidentType
from .state import GameState


def resolve_murder(culprit: Character, incident: Incident, game_state: GameState):
    if not culprit.alive:
        print(f"🟢 The murder incident does not happen on day {game_state.day}")
        return

    others = [
        c for c in game_state.characters
        if c.alive and c.location == culprit.location and c != culprit
    ]
    if len(others) >= 1:
        todays_action = game_state.actions[game_state.day]
        incident_choice = todays_action["incident_choices"][0]
        target = incident_choice.target
        target_character = next((c for c in others if c.name == target), None)
        if target_character is None:
            raise ValueError(f"Murder target not in same location as Culprit")
        target_character.alive = False
        print(f"💀 {culprit.name} (Murder Culprit) murdered {target_character.name} at {culprit.location.name}")
    else:
        print(f"🟢 The murder incident does not happen on day {game_state.day}")

def resolve_suicide(culprit: Character, incident: Incident, game_state: GameState):
    if not culprit.alive:
        print(f"🟢 The suicide incident does not happen on day {game_state.day}")
        return
    else:
        culprit.alive = False
        print(f"💀 {culprit.name} committed suicide")

INCIDENT_EFFECTS = {
    IncidentType.MURDER: resolve_murder,
    IncidentType.SUICIDE: resolve_suicide,
    # Add others as needed
}
