import { useState } from "react";
import { GameStateResponse, ActionPayload, Role } from "../types";

const ACTION_TYPES = [
  { label: "Move Character Horizontally", value: "MOVE_HORIZONTAL" },
  { label: "Move Character Vertically", value: "MOVE_VERTICAL" },
  { label: "Add Goodwill", value: "ADD_GOODWILL" },
  { label: "Add Paranoia", value: "ADD_PARANOIA" },
];

export function ActionForm({
  gameState,
  onSubmit,
}: {
  gameState: GameStateResponse;
  onSubmit: (actions: {
    mastermind: ActionPayload[];
    protagonist: ActionPayload[];
    incident_choices: ActionPayload[];
  }) => void;
}) {
  const characters = gameState.characters;

  const [mastermind, setMastermind] = useState<ActionPayload[]>([]);
  const [protagonist, setProtagonist] = useState<ActionPayload[]>([]);
  const [incidentChoices, setIncidentChoices] = useState<ActionPayload[]>([]);

  const [selectedRole, setSelectedRole] = useState<Role>("mastermind");
  const [selectedCharacter, setSelectedCharacter] = useState<string>(characters[0]);
  const [selectedActionType, setSelectedActionType] = useState<string>(ACTION_TYPES[0].value);

  const addAction = () => {
    const action: ActionPayload = {
      action_type: selectedActionType,
      target: selectedCharacter,
    };

    if (selectedRole === "mastermind") setMastermind((prev) => [...prev, action]);
    else setProtagonist((prev) => [...prev, action]);
  };

  return (
    <div>
      <h3>Submit Actions</h3>

      <div>
        <h4>1. Select Role</h4>
        {(["mastermind", "protagonist"] as Role[]).map((role) => (
          <label key={role}>
            <input
              type="radio"
              name="role"
              value={role}
              checked={selectedRole === role}
              onChange={() => setSelectedRole(role)}
            />
            {role}
          </label>
        ))}
      </div>

      <div>
        <h4>2. Select Character</h4>
        {characters.map((char) => (
          <label key={char}>
            <input
              type="radio"
              name="character"
              value={char}
              checked={selectedCharacter === char}
              onChange={() => setSelectedCharacter(char)}
            />
            {char}
          </label>
        ))}
      </div>

      <div>
        <h4>3. Select Action</h4>
        {ACTION_TYPES.map(({ label, value }) => (
          <label key={value}>
            <input
              type="radio"
              name="actionType"
              value={value}
              checked={selectedActionType === value}
              onChange={() => setSelectedActionType(value)}
            />
            {label}
          </label>
        ))}
      </div>

      <div style={{ marginTop: "1em" }}>
        <button onClick={addAction}>Add Action</button>
      </div>

      <div style={{ marginTop: "1em" }}>
        <button onClick={() =>
          onSubmit({
            mastermind,
            protagonist,
            incident_choices: incidentChoices,
          })
        }>
          Submit
        </button>
      </div>

      <div style={{ marginTop: "1em" }}>
        <h4>Current Actions</h4>
        <pre>{JSON.stringify({ mastermind, protagonist, incidentChoices }, null, 2)}</pre>
      </div>
    </div>
  );
}
