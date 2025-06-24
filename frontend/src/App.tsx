import { useEffect, useState } from "react";
import { GameView } from "./components/GameView";
import { ActionForm } from "./components/ActionForm";
import { GameStateResponse, Role, ActionPayload } from "./types";
import { startGame, getGameState, submitActions } from "./api";

function App() {
  const [gameId, setGameId] = useState<string>("");
  const [state, setState] = useState<GameStateResponse | null>(null);

  useEffect(() => {
    startGame().then(id => {
      setGameId(id);
      getGameState(id).then(setState);
    });
  }, []);

  const handleSubmit = async (actions: Record<Role, ActionPayload[]>) => {
    if (!gameId) return;
    const newState = await submitActions({ game_id: gameId, actions });
    setState(newState);
  };

  return (
    <div>
      <h1>🌀 Disaster Cycler</h1>
      {state && <GameView state={state} />}
      <ActionForm onSubmit={handleSubmit} />
    </div>
  );
}

export default App;
