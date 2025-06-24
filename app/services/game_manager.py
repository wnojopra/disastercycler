import uuid
from engine.yaml_loader import load_script_from_yaml
from engine.simulation import simulate_day
from engine.state import GameState
from engine.models import Action, ActionSource, ActionTargetType, ActionType, IncidentChoice, IncidentType, Location, TurnData
from app.models.api_models import GameStateResponse, ActionPayload

SCRIPT_PATH = "scripts/the_first_script/script.yaml"

def to_engine_action(source: ActionSource, payload: ActionPayload) -> Action:
    action_type = ActionType[payload.action_type]

    if payload.target.lower() in {loc.value for loc in Location}:
        target_type = ActionTargetType.LOCATION
    else:
        target_type = ActionTargetType.CHARACTER

    return Action(
        source=source,
        type=action_type,
        target_type=target_type,
        target=payload.target
    )

class GameManager:
    def __init__(self):
        self.sessions: dict[str, GameState] = {}

    def start_game(self) -> str:
        game_id = str(uuid.uuid4())
        script = load_script_from_yaml(SCRIPT_PATH)
        game_state = GameState(
            day=1,
            loop_count=1,
            days_per_loop=script.days_per_loop,
            max_loops=script.max_loops,
            characters=script.characters,
            incidents=script.incidents,
            actions={},  # We'll add actions dynamically
        )
        self.sessions[game_id] = game_state
        return game_id

    def apply_actions(self, game_id: str, actions: dict) -> GameStateResponse:
        if game_id not in self.sessions:
            raise ValueError("Game not found")

        game_state = self.sessions[game_id]
        day = game_state.day

        all_actions = []
        for role_key in ["mastermind", "protagonist"]:
            role_enum = ActionSource(role_key)
            for payload in actions.get(role_key, []):
                all_actions.append(to_engine_action(role_enum, payload))

        incident_choices = []
        for ic_payload in actions.get("incident_choices", []):
            incident_choices.append(IncidentChoice(
                type=IncidentType(ic_payload["type"]),
                target=ic_payload["target"]
            ))

        game_state.actions[day] = TurnData(
            actions=all_actions,
            incident_choices=incident_choices or None
        )

        simulate_day(game_state)
        return GameStateResponse.from_game_state(game_id, game_state)

    def get_game_state(self, game_id: str) -> GameStateResponse | None:
        game_state = self.sessions.get(game_id)
        if not game_state:
            return None
        return GameStateResponse.from_game_state(game_id, game_state)
