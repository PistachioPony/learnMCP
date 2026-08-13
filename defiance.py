# This module takes care of the Defiance Mechanic
# When a card called from the Fortuneteller's Hand takes 
# a dark turn in the narration, the player can call Defiance - "Not like this!"
# A Yahtzee roll up to 3 times to buy not IF it happens but How, When, or Whom the
# fate falls on. Each roll gives the player a debt card.  
# If the player gets 5 of a kind, then they are allowed full authorship of the grounding.

import random
from collections import Counter
from typing import Literal

import debt
from hand_deck import draw_from_hand_deck

_dice: list[int] = []
_rolls_taken = 0


def _is_small_straight(dice: list[int]) -> bool:
    distinct = set(dice)
    return any(run.issubset(distinct) for run in ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}))


def _evaluate(dice: list[int]) -> tuple[str, str] | None:
    counts = sorted(Counter(dice).values(), reverse=True)

    if counts[0] == 5:
        return ("five of a kind", "seize the pen — full authorship of the landing, within the card")
    if counts[:2] == [3, 2]:
        return ("full house", "take the cup — the WHOM, a different head, yours included")
    if _is_small_straight(dice):
        return ("small straight", "stay the hand — the WHEN, delayed one full scene")
    if counts[0] >= 3:
        return ("three of a kind", "turn the blade — the HOW, manner changes; target and moment keep")
    return None


def defy_roll(keep: list[Literal[1, 2, 3, 4, 5, 6]] | None = None) -> dict:
    """Roll the defiance dice, keeping any values specified from the current dice, up to three rolls total."""
    global _dice, _rolls_taken

    keep = keep or []

    if _rolls_taken >= 3:
        raise ValueError("Already rolled three times — call defy_resolve() to finish the ritual.")

    if _dice:
        available = Counter(_dice)
        for value, count in Counter(keep).items():
            if available[value] < count:
                raise ValueError(f"Can't keep {count} dice showing {value} — current dice are {sorted(_dice)}.")
    elif keep:
        raise ValueError("No dice to keep yet — the first roll must start with keep=[].")

    new_rolls = [random.randint(1, 6) for _ in range(5 - len(keep))]
    _dice = keep + new_rolls
    _rolls_taken += 1

    result = _evaluate(_dice)

    return {
        "dice": sorted(_dice),
        "rolls_taken": _rolls_taken,
        "rolls_remaining": 3 - _rolls_taken,
        "current_pattern": result[0] if result else None,
        "current_bend": result[1] if result else None,
    }


def defy_resolve() -> dict:
    """Lock in the current dice as final, deal one debt card per roll taken, and reset the ritual."""
    global _dice, _rolls_taken

    if not _dice:
        raise ValueError("No defiance ritual in progress — call defy_roll() first.")

    final_dice = sorted(_dice)
    rolls_taken = _rolls_taken
    result = _evaluate(final_dice)

# Adding a card from each roll into the debt row.
    dealt = []
    for _ in range(rolls_taken):
        card = draw_from_hand_deck()
        debt.DEBT_ROW.append(card)
        dealt.append(card)

    _dice = []
    _rolls_taken = 0

    return {
        "final_dice": final_dice,
        "rolls_taken": rolls_taken,
        "pattern": result[0] if result else None,
        "bend": result[1] if result else None,
        "debt_dealt": dealt,
    }
