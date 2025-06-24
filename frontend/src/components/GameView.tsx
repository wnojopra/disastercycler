import { CharacterState, GameStateResponse } from "../types";

export function GameView({ state }: { state: GameStateResponse }) {
  return (
    <div>
      <h2>Loop {state.loop_count}, Day {state.day}</h2>
      {state.game_result && <h3>🏁 Result: {state.game_result}</h3>}
      <table>
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Paranoia</th><th>Goodwill</th><th>Intrigue</th><th>Status</th><th>Role</th>
          </tr>
        </thead>
        <tbody>
          {state.characters.map((char: CharacterState) => (
            <tr key={char.name}>
              <td>{char.name}</td>
              <td>{char.location}</td>
              <td>{char.paranoia}</td>
              <td>{char.goodwill}</td>
              <td>{char.intrigue}</td>
              <td>{char.alive ? "Alive" : "Dead"}</td>
              <td>{char.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
