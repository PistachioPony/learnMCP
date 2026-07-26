import random
from typing import Literal

from oracle_data import ORACLE_GRID, SUITS

SUIT_PILES = {
    suit: random.sample([card for card in ORACLE_GRID if card["suit"] == suit], 13)
    for suit in SUITS
}


def draw_cross_card(suit: Literal["♥", "♦", "♣", "♠"]) -> dict:
    """Draw a card for the Sitting's cross, blind, from the given suit's pile."""
    pile = SUIT_PILES[suit]
    if not pile:
        raise ValueError(f"No cards left in the {suit} pile — it's already been drawn from this Sitting.")
    return pile.pop()
