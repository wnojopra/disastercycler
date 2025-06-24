import uuid
from engine.yaml_loader import load_script_from_yaml
from engine.simulation import create_starting_game_state, simulate_day
from engine.state import GameState
from engine.models import Action, ActionType, IncidentType
from app.models.api_models import SubmitActionsRequest, GameStateResponse, ActionPayload

SCRIPT_PATH = "scripts/the_first_script/script.yaml"

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
        game_state.actions[game_state.day] = {
            role: [Action(type=self._parse_action_type(a["type"]), target=a["target"]) for a in action_list]
            for role, action_list in actions.items()
        }

        simulate_day(game_state)
        return GameStateResponse.from_game_state(game_id, game_state)

    def get_game_state(self, game_id: str) -> GameStateResponse | None:
        game_state = self.sessions.get(game_id)
        if not game_state:
            return None
        return GameStateResponse.from_game_state(game_id, game_state)

    def _parse_action_type(self, value: str):
        try:
            return ActionType[value]
        except KeyError:
            return IncidentType[value]
