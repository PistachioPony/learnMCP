import random
from typing import Literal

from oracle_data import ORACLE_GRID, SUITS


def _fresh_suit_piles() -> dict[str, list[dict]]:
    return {
        suit: random.sample([card for card in ORACLE_GRID if card["suit"] == suit], 13)
        for suit in SUITS
    }


SUIT_PILES = _fresh_suit_piles()

CROSS: dict[str, dict] = {}
CHARACTER_NAME: str | None = None
GOAL: dict | None = None


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


def draw_goal_card() -> dict:
    """Deal the Goal: reshuffle what's left of fate's deck and draw one card face up."""
    global GOAL
    if len(CROSS) < 4:
        raise ValueError("The cross isn't complete yet — draw all four cross positions before dealing the Goal.")
    if GOAL is not None:
        raise ValueError("The Goal has already been dealt for this Sitting.")

    remainder = [(suit, card) for suit, pile in SUIT_PILES.items() for card in pile]
    suit, card = random.choice(remainder)
    SUIT_PILES[suit].remove(card)
    GOAL = card
    return GOAL
