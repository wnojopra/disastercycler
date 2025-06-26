# Disaster Cycler

This is a digital simulation engine for the board game *Tragedy Looper*, implemented in Python. The project models core game logic — including characters, hidden roles, incidents, and looping timelines — and powers an interactive API for web or CLI-based gameplay.

## 🧠 Project Goals

- Simulate Protagonist vs Mastermind gameplay
- Load characters, roles, incidents, and actions from YAML scripts
- Resolve daily actions and role-based effects (e.g., Serial Killer, Brain)
- Track win/loss conditions like Key Person death or loop exhaustion
- Expose a FastAPI backend for a future web frontend


## 📁 Project Structure
```graphql
disastercycler/
├── app/ # FastAPI app and API routes
│ ├── main.py # FastAPI entrypoint
│ ├── api/routes.py # /start_game, /submit_actions, /game_state
│ ├── services/game_manager.py # Game session lifecycle manager
│ └── models/api_models.py # Pydantic request/response models
│
├── engine/ # Core game engine
│ ├── simulation.py # CLI driver
│ ├── models.py # Characters, Actions, Roles, Enums
│ ├── state.py # GameState class
│ ├── engine.py # Action and role resolution
│ ├── victory_checker.py # Win/loss detection
│ ├── incident_effects.py # Incident-specific outcomes
│ ├── role_effects.py # Role-specific behaviors
│ └── yaml_loader.py # Script/action YAML deserialization
│
├── scripts/ # YAML-based Tragedy Looper scripts
│ └── the_first_script/
│ ├── script.yaml
│ └── actions.yaml
│
├── tests/ # (Coming soon) Unit/integration tests
└── requirements.txt
```

## 🚀 How to Run

### 📦 Install dependencies

In order to not overwrite the installed packages of your system Python, we suggest creating a python virtual environment for dependencies.

```bash
# This creates a directory named venv/
python3 -m venv venv

# This modifies your shell's `PATH` to use Python and pip from `venv/`
source venv/bin/activate

# This installs the project dependcies into venv Python
pip install -r requirements.txt
pip install -e .
```

Once you have activated the virtual environment and installed requirements, you can run the below commands to run the simulation and backend service. 


### 🧪 Run the Simulation from CLI
From the root directory:

```bash
python -m engine.simulation the_first_script actions
```
This runs through all game days using the specified script and actions file.

Example output:

```css
💀 Student A (Serial Killer) killed Nurse B at SCHOOL  
❌ Nurse B (Key Person) is dead — Mastermind wins!  
🏁 Game Over — Mastermind Win
```

### 🌐 Start the FastAPI Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Then open: http://localhost:8000/docs for interactive Swagger API.

### 🔍 Run tests
```bash
pytest
```


## ✅ Features
- Character model with paranoia, goodwill, intrigue, and disallowed locations

- Action system: movement, paranoia/goodwill modifiers

- Role resolution system (e.g., Serial Killer, Brain)

- Incident resolution (e.g., Murder, Suicide)

- Victory checker for Mastermind vs Protagonist outcomes

- YAML scripting system for user-authored scenarios

- REST API for interactive gameplay via frontend or remote clients

## 🧭 Roadmap
- Loop resets and memory wiping

- Role logic: Witch, Time Traveller, Lover, etc.

- Turn-based React/TypeScript frontend

- Game state persistence (e.g., Redis or DB)

- Multiple concurrent game sessions

- Frontend-authenticated multiplayer mode

## 🙏 Acknowledgments
This project is inspired by the board game Tragedy Looper designed by BakaFire and published by Z-Man Games. This is an unofficial fan-made implementation for educational and personal use only.

## 📜 License
MIT License
