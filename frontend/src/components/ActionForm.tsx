import { useState } from "react";
import { ActionPayload, Role } from "../types";

export function ActionForm({ onSubmit }: {
  onSubmit: (actions: Record<Role, ActionPayload[]>) => void;
}) {
  const [mastermind, setMastermind] = useState<ActionPayload[]>([]);
  const [protagonist, setProtagonist] = useState<ActionPayload[]>([]);
  const [incidentChoices, setIncidentChoices] = useState<ActionPayload[]>([]);

  const addAction = (role: Role, type: string, target: string) => {
    const action = { type, target };
    if (role === "mastermind") setMastermind(prev => [...prev, action]);
    else if (role === "protagonist") setProtagonist(prev => [...prev, action]);
    else setIncidentChoices(prev => [...prev, action]);
  };

  return (
    <div>
      <h3>Submit Actions</h3>
      <button onClick={() => onSubmit({ mastermind, protagonist, incident_choices: incidentChoices })}>
        Submit
      </button>
      {/* For dev: quick add buttons */}
      <div>
        <button onClick={() => addAction("mastermind", "ADD_PARANOIA", "Girl Student")}>
          Add Paranoia to Girl Student (Mastermind)
        </button>
        <button onClick={() => addAction("protagonist", "ADD_GOODWILL", "Office Worker")}>
          Add Goodwill to Office Worker (Protagonist)
        </button>
        <button onClick={() => addAction("incident_choices", "MURDER", "Girl Student")}>
          Trigger Murder on Girl Student
        </button>
      </div>
    </div>
  );
}
