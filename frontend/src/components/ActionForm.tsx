import { useState } from "react";
import { ActionPayload, Role, CharacterState } from "../types";

// Define the actions available to players
const PLAYER_ACTIONS = ["ADD_GOODWILL", "ADD_INTRIGUE", "MOVE_VERTICAL", "MOVE_HORIZONTAL"];
const MASTERMIND_ACTIONS = ["ADD_PARANOIA"];

export function ActionForm({
  onSubmit,
  characters,
}: {
  onSubmit: (actions: Record<Role, ActionPayload[]>) => void;
  characters: CharacterState[];
}) {
  // State for the actions that will be submitted
  const [mastermindActions, setMastermindActions] = useState<ActionPayload[]>([]);
  const [protagonistActions, setProtagonistActions] = useState<ActionPayload[]>([]);

  // State for the current action being built in the form
  const [currentRole, setCurrentRole] = useState<"mastermind" | "protagonist">("mastermind");
  const [currentActionType, setCurrentActionType] = useState(MASTERMIND_ACTIONS[0]);
  const [currentTarget, setCurrentTarget] = useState(characters[0]?.name || "");

  const handleAddAction = () => {
    if (!currentTarget) return;
    const newAction = { action_type: currentActionType, target: currentTarget };
    
    if (currentRole === 'mastermind' && mastermindActions.length < 3) {
      setMastermindActions(prev => [...prev, newAction]);
    } else if (currentRole === 'protagonist' && protagonistActions.length < 3) {
      setProtagonistActions(prev => [...prev, newAction]);
    }
  };
  
  const handleFormSubmit = () => {
    onSubmit({
      mastermind: mastermindActions,
      protagonist: protagonistActions,
      // For now, incident_choices is empty. Can be added later.
      incident_choices: [] 
    });
    // Clear actions after submitting
    setMastermindActions([]);
    setProtagonistActions([]);
  };
  
  const actionOptions = currentRole === 'mastermind' ? MASTERMIND_ACTIONS : PLAYER_ACTIONS;

  return (
    <div style={{ border: '1px solid black', padding: '10px', marginTop: '20px' }}>
      <h3>Build Your Actions</h3>
      
      {/* --- The Action Builder UI --- */}
      <div>
        <select value={currentRole} onChange={e => setCurrentRole(e.target.value as any)}>
          <option value="mastermind">Mastermind</option>
          <option value="protagonist">Protagonist</option>
        </select>
        <select value={currentActionType} onChange={e => setCurrentActionType(e.target.value)}>
          {actionOptions.map(act => <option key={act} value={act}>{act}</option>)}
        </select>
        <select value={currentTarget} onChange={e => setCurrentTarget(e.target.value)}>
          {characters.map(char => <option key={char.name} value={char.name}>{char.name}</option>)}
        </select>
        <button onClick={handleAddAction}>Add Action</button>
      </div>

      {/* --- Display pending actions --- */}
      <div>
        <h4>Pending Mastermind Actions ({mastermindActions.length}/3):</h4>
        <ul>{mastermindActions.map((a, i) => <li key={i}>{a.action_type} on {a.target}</li>)}</ul>
      </div>
      <div>
        <h4>Pending Protagonist Actions ({protagonistActions.length}/3):</h4>
        <ul>{protagonistActions.map((a, i) => <li key={i}>{a.action_type} on {a.target}</li>)}</ul>
      </div>

      {/* --- The final submit button --- */}
      <button onClick={handleFormSubmit} style={{ marginTop: '20px', padding: '10px' }}>
        SUBMIT DAY'S ACTIONS
      </button>
    </div>
  );
}