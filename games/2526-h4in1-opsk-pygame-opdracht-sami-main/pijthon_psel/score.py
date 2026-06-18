from .setup import ROOT
from typing import * # type: ignore
import json

SCORE_PATH: str = f"{ROOT}/assets/scoreboard/"
GAME_SCORE: str = "game.json"
DUOS_SCORE: str = "duos.json"
FREEPLAY_SCORE: str = "freeplay.json"

def add_game_entry(name: str, score: int) -> None:
    gs: List[Tuple[str, int]] = get_game()
    gs.append((name, score))
    json.dump(gs, open(SCORE_PATH + GAME_SCORE, "w+"))
    pass

def add_freeplay_entry(name: str, score: int) -> None:
    gs: List[Tuple[str, int]] = get_freeplay()
    gs.append((name, score))
    json.dump(gs, open(SCORE_PATH + FREEPLAY_SCORE, "w+"))
    pass

def add_duos_entry(name: str, score: int) -> None:
    gs: List[Tuple[str, int]] = get_duos()
    gs.append((name, score))
    json.dump(gs, open(SCORE_PATH + DUOS_SCORE, "w+"))
    pass

def get_game() -> List[Tuple[str, int]]:
    with open(SCORE_PATH + GAME_SCORE, "r") as file:
        gs: List[Tuple[str, int]] = json.load(file)
        return gs
    pass

def get_freeplay() -> List[Tuple[str, int]]:
    with open(SCORE_PATH + FREEPLAY_SCORE, "r") as file:
        gs: List[Tuple[str, int]] = json.load(file)
        return gs
    pass

def get_duos() -> List[Tuple[str, int]]:
    with open(SCORE_PATH + DUOS_SCORE, "r") as file:
        gs: List[Tuple[str, int]] = json.load(file)
        return gs
    pass
