# Disaster Cycler
This is a digital simulation engine for the board game Tragedy Looper, implemented in Python. The project models core game logic — including characters, hidden roles, programmed actions, and looping timelines — as a foundation for an eventual web-based version.

## 🧠 Project Goals
- Simulate Protagonist vs Mastermind gameplay

- Load characters, actions, and scripts from YAML files

- Resolve daily actions and role-based effects (e.g., Serial Killer, Key Person)

- Check for win/loss conditions like Key Person death or Butterfly Effect

- Serve as a backend engine for a future FastAPI + React frontend

## 📁 Project Structure
```graphql
Copy
Edit
tragedy_looper/
├── data/                  # YAML files for characters, actions, etc.
├── models.py              # Core data classes (Character, RoleType, etc.)
├── state.py               # GameState object to track game progress
├── engine.py              # Main logic: action resolution, role effects
├── role_effects.py        # Per-role behavior (e.g., serial_killer kills)
├── victory_checker.py     # Centralized win/loss condition logic
├── action_loader.py       # Loads YAML-defined actions
├── character_loader.py    # Loads YAML-defined characters
├── simulation.py          # CLI tool to simulate 1 day of gameplay
└── tests/                 # (Coming soon)
```

## 🚀 Running a Simulation
1. Install dependencies (requires Python 3.10+):

```bash
pip install pyyaml
```
2. Run a day-1 simulation:

```bash
python simulation.py
```

3. Example output:

```css
💀 Student A (Serial Killer) killed Nurse B at SCHOOL  
❌ Nurse B (Key Person) is dead — Mastermind wins!  
🏁 Game Over — Mastermind Win
```

## ✅ Current Features
- Character model with role, location, paranoia, goodwill, etc.

- Action resolution (move, add_paranoia, add_goodwill)

- Role effects via registry (e.g., Serial Killer kills if alone with one person)

- Win/loss checker (e.g., Key Person death triggers Mastermind win)

- YAML-based input system for characters and action scripting

## 🧭 Roadmap
 - Incident triggering + resolution

 - Loop resets

 - Role logic: Cultist, Brain, Witch, etc.

 - YAML-based full script system (with incidents + roles)

 - FastAPI backend with REST endpoints

 - React/TypeScript frontend

## 🙏 Acknowledgments
This project is inspired by the board game Tragedy Looper designed by BakaFire and published by Z-Man Games. This is an unofficial fan-made implementation for educational and personal use only.

## 📜 License
MIT License
