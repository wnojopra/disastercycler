import axios from "axios";
import { SubmitActionsRequest, GameStateResponse } from "./types";

// const BASE_URL = "http://localhost:8000";
const BASE_URL = "https://fantastic-carnival-rv6vprgrq5fpwx-8000.app.github.dev";

export async function startGame(): Promise<string> {
  const res = await axios.post(`${BASE_URL}/start_game`);
  return res.data;
}

export async function getGameState(gameId: string): Promise<GameStateResponse> {
  const res = await axios.get(`${BASE_URL}/game_state`, { params: { game_id: gameId } });
  return res.data;
}

export async function submitActions(payload: SubmitActionsRequest): Promise<GameStateResponse> {
  const res = await axios.post(`${BASE_URL}/submit_actions`, payload);
  return res.data;
}
