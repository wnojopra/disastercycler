from fastapi import APIRouter, HTTPException

from app.models.api_models import GameStateResponse, SubmitActionsRequest
from app.services.game_manager import GameManager

router = APIRouter()
game_manager = GameManager()


@router.post("/start_game")
def start_game() -> str:
    return game_manager.start_game()


@router.post("/submit_actions")
def submit_actions(req: SubmitActionsRequest) -> GameStateResponse:
    try:
        return game_manager.apply_actions(req.game_id, req.actions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/game_state", response_model=GameStateResponse)
def get_game_state(game_id: str):
    state = game_manager.get_game_state(game_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return state
