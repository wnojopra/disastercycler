import { CharacterState, GameStateResponse } from "../types";
import { CharacterCard } from "./CharacterCard";
import './GameView.css'; // Add a new CSS file for the view

// All possible locations, you might get this from your engine or define it here
const ALL_LOCATIONS = ["HOSPITAL", "SHRINE", "CITY", "SCHOOL"];

export function GameView({ state }: { state: GameStateResponse }) {
  return (
    <div className="game-view-container">
      <h2>Loop {state.loop_count}, Day {state.day}</h2>
      {state.game_result && <h3>🏁 Result: {state.game_result}</h3>}
      
      <div className="game-board">
        {ALL_LOCATIONS.map(location => (
          <div key={location} className="location-box">
            <h3>{location.charAt(0).toUpperCase() + location.slice(1).toLowerCase()}</h3>
            <div className="character-container">
              {state.characters
                .filter(char => char.location === location)
                .map(char => <CharacterCard key={char.name} char={char} />)
              }
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}