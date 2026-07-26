import random

from oracle_data import ORACLE_GRID

HAND_DECK = random.sample(ORACLE_GRID, len(ORACLE_GRID))


def draw_from_hand_deck() -> dict:
    """Draw the top card of the Fortuneteller's Hand deck."""
    if not HAND_DECK:
        raise ValueError("The Fortuneteller's Hand deck is empty.")
    return HAND_DECK.pop()
