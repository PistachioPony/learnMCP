import json
from pathlib import Path

import debt
import hand_deck
import journal_of_fate
import thesitting

SAVE_FILE = Path(__file__).parent / "save.json"


def save_game() -> dict:
    """Save the current game to disk, overwriting any existing save."""
    state = {
        "character_name": thesitting.CHARACTER_NAME,
        "cross": thesitting.CROSS,
        "goal": thesitting.GOAL,
        "suit_piles": thesitting.SUIT_PILES,
        "debt_row": debt.DEBT_ROW,
        "hand_deck": hand_deck.HAND_DECK,
        "journal": journal_of_fate.JOURNAL,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)
    return state


def load_game() -> None:
    """Load a saved game from disk into module state, if a save file exists."""
    if not SAVE_FILE.exists():
        return

    with open(SAVE_FILE) as f:
        state = json.load(f)

    thesitting.CHARACTER_NAME = state["character_name"]
    thesitting.CROSS = state["cross"]
    thesitting.GOAL = state["goal"]
    thesitting.SUIT_PILES = state["suit_piles"]
    debt.DEBT_ROW = state["debt_row"]
    hand_deck.HAND_DECK = state["hand_deck"]
    journal_of_fate.JOURNAL = state["journal"]


def reset_game() -> None:
    """Wipe all game state and start a full new game, not just a new Sitting."""
    thesitting.CHARACTER_NAME = None
    thesitting.CROSS = {}
    thesitting.GOAL = None
    thesitting.SUIT_PILES = thesitting._fresh_suit_piles()
    debt.DEBT_ROW = []
    hand_deck.HAND_DECK = hand_deck._fresh_hand_deck()
    journal_of_fate.JOURNAL = []
