export type Role = "mastermind" | "protagonist" | "incident_choices";

export interface ActionPayload {
  type: string;
  target: string;
}

export interface SubmitActionsRequest {
  game_id: string;
  actions: Record<Role, ActionPayload[]>;
}

export interface CharacterState {
  name: string;
  location: string;
  paranoia: number;
  goodwill: number;
  intrigue: number;
  alive: boolean;
  role: string;
}

export interface GameStateResponse {
  game_id: string;
  day: number;
  loop_count: number;
  game_result: string | null;
  characters: CharacterState[];
}
