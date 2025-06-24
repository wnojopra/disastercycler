from pydantic import BaseModel
from typing import List, Dict, Literal
from engine.state import GameState

class ActionPayload(BaseModel):
    action_type: str
    target: str

class SubmitActionsRequest(BaseModel):
    game_id: str
    actions: Dict[Literal["mastermind", "protagonist", "incident_choices"], List[ActionPayload]]

class CharacterState(BaseModel):
    name: str
    location: str
    paranoia: int
    goodwill: int
    intrigue: int
    alive: bool
    role: str

class GameStateResponse(BaseModel):
    game_id: str
    day: int
    loop_count: int
    game_result: str | None
    characters: List[CharacterState]

    @staticmethod
    def from_game_state(game_id: str, game_state: GameState) -> "GameStateResponse":
        return GameStateResponse(
            game_id=game_id,
            day=game_state.day,
            loop_count=game_state.loop_count,
            game_result=game_state.game_result,
            characters=[
                CharacterState(
                    name=c.name,
                    location=c.location.name,
                    paranoia=c.paranoia,
                    goodwill=c.goodwill,
                    intrigue=c.intrigue,
                    alive=c.alive,
                    role=c.role.name
                )
                for c in game_state.characters
            ]
        )
