# This module is "The Sitting", the first encounter with The Fortuneteller. 
# It helps the player create a character and a goal for the game.

import random
from typing import Literal

from oracle_data import ORACLE_GRID, SUITS


# each suit's 13-card pile, freshly shuffled at module load.
SUIT_PILES = {
    suit: random.sample([card for card in ORACLE_GRID if card["suit"] == suit], 13)
    for suit in SUITS
}

# Dict that holds the character info for the game.
CROSS: dict[str, dict] = {}

# Character name string
CHARACTER_NAME: str | None = None

# The goal dict
GOAL: dict | None = None


def name_character(player_name: str) -> dict:
    """Set the name of the character being created for a new Sitting.

    Already called automatically, once, when the start_game prompt runs —
    you typically won't need to call this tool yourself. It exists as a
    standalone tool mainly so get_sheet and other tools have a name to
    validate against. Call it directly only if you need to (re)name a
    character outside the normal start_game flow.

    player_name: the player-chosen name for their character. No format
    constraints.

    Not idempotent: overwrites the shared character name each time it's
    called, with no confirmation or uniqueness check. Returns
    {"player_name": player_name}.
    """
    global CHARACTER_NAME
    CHARACTER_NAME = player_name
    return {"player_name": player_name}

# Let's draw the cards and Claude will show them to the player for them to interpret.
def draw_cross_card(
    suit: Literal["♥", "♦", "♣", "♠"],
    position: Literal["Motivation", "Seek", "Carry", "Ends"],
) -> dict:
    """Draw one card, blind, into a position on the Sitting's cross — the four-drive character-creation spread built once at the start of every campaign.

    Call once per drive during the Sitting, after the player has chosen a
    suit for that drive: Motivation, then Seek, then Carry, then Ends, in
    that order. Each of the four positions and each of the four suits can
    only be used once each — calling this with a position or suit already
    used raises ValueError. "Blind" means the card is drawn face-down from
    the matching suit's own 13-card pile without looking; don't reveal its
    phrase to the player until all four drives have a card.

    suit: which of the four card suits (♥ Hearts, ♦ Diamonds, ♣ Clubs,
    ♠ Spades) the player chose for this drive — each suit represents a
    different domain of meaning (love/loyalty, wealth/ambition,
    labor/growth, death/conflict).
    position: which of the four drives this card fills — Motivation, Seek,
    Carry, or Ends.

    Not idempotent: mutates the shared cross and removes a card from the
    suit's pile. Returns the drawn card as a dict with rank, suit,
    suit_name, domain, rank_meaning, and phrase.
    """
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

# Now let's give the player a prompt for their character's goal 
def draw_goal_card() -> dict:
    """Deal the Goal: draw one card face-up from whatever's left across all four suit piles, once all four drives have been drawn.

    Call once, during the Sitting, right after all four calls to
    draw_cross_card are done (one per drive: Motivation, Seek, Carry, Ends)
    and the player has described their character. Unlike draw_cross_card,
    this draws from the combined remainder of all four suit piles at once,
    not one specific suit — and it's revealed to the player immediately,
    not held back. After dealing it and asking what it means, pass the
    player's answer to record_goal_interpretation.

    Takes no parameters. Raises ValueError if called before all four cross
    positions are filled, or if a Goal has already been dealt this Sitting.
    Not idempotent: mutates the shared Goal and the relevant suit pile.
    Returns the drawn card as a dict with rank, suit, suit_name, domain,
    rank_meaning, and phrase.
    """
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

# Claude now reflects back to the player the goal interpretation.
def record_goal_interpretation(interpretation: str) -> dict:
    """Save the player-and-Claude-agreed meaning of the Goal card onto the Goal, for later reference.

    Call once, during the Sitting, right after the player has answered what
    the Goal means and Claude has reflected that answer back in a sentence
    or two — pass that reflected sentence in. This becomes the saved
    reference that complete_goal later checks against (via get_sheet's
    'goal' field) to judge whether a moment in play genuinely resolves the
    Goal.

    interpretation: a plain-language sentence or two capturing what the
    Goal means for this character — Claude's own reflected summary, not a
    verbatim quote of the player's answer.

    Raises ValueError if called before draw_goal_card has dealt a Goal.
    Not idempotent: overwrites any existing interpretation on the shared
    Goal. Returns the full updated Goal card dict, including the new
    'interpretation' field.
    """
    if GOAL is None:
        raise ValueError("The Goal hasn't been dealt yet — draw it before recording what it means.")
    GOAL["interpretation"] = interpretation
    return GOAL
