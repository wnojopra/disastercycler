from dataclasses import dataclass
from typing import List, Optional

from models import Character, Incident, AllActionsByDay


@dataclass
class GameState:
    day: int
    loop_count: int
    max_loops: int
    characters: List[Character]
    incidents: List[Incident]
    actions: AllActionsByDay
    game_result: Optional[str] = None  # "protagonists_win", "mastermind_win", or None


    def print_characters(self):
        for char in self.characters:
            message = f"{char.name} is at {char.location}, paranoia={char.paranoia}, goodwill={char.goodwill}"
            if not char.alive:
                message += ", status=DEAD"
            print(message)