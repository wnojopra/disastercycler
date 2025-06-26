import { CharacterState } from "../types";
import './CharacterCard.css';

export function CharacterCard({ char }: { char: CharacterState }) {
  const cardClass = `character-card ${char.alive ? '' : 'dead'}`;

  return (
    <div className={cardClass}>
      <h4>{char.name}</h4>
      <p>Role: {char.role}</p>
      <p>Paranoia: {char.paranoia} | Goodwill: {char.goodwill} | Intrigue: {char.intrigue}</p>
    </div>
  );
}