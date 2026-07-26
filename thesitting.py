import random
from typing import Literal

from oracle_data import ORACLE_GRID, SUITS

SUIT_PILES = {
    suit: random.sample([card for card in ORACLE_GRID if card["suit"] == suit], 13)
    for suit in SUITS
}

CROSS: dict[str, dict] = {}
CHARACTER_NAME: str | None = None


def name_character(player_name: str) -> dict:
    """Name the character being created at the Sitting."""
    global CHARACTER_NAME
    CHARACTER_NAME = player_name
    return {"player_name": player_name}


def draw_cross_card(
    suit: Literal["♥", "♦", "♣", "♠"],
    position: Literal["Motivation", "Ends", "Seek", "Carry"],
) -> dict:
    """Draw a card for the Sitting's cross, blind, from the given suit's pile, into the given position."""
    if position in CROSS:
        raise ValueError(f"{position} already has a card — each position is only drawn once.")
    if any(card["suit"] == suit for card in CROSS.values()):
        raise ValueError(f"{suit} is already assigned to another position — each suit maps to exactly one position.")

    pile = SUIT_PILES[suit]
    if not pile:
        raise ValueError(f"No cards left in the {suit} pile — it's already been drawn from this Sitting.")

    card = pile.pop()
    CROSS[position] = card
    return card
