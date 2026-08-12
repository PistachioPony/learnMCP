# This is the Omens module for the Omens dice mechanic AND the place where Claude 
# flips the goal to completed.
# When a player narrates to the point where they are confronted with an unknown,
# that is, something that cannot have insight into: Other Hearts, Hidden Things,
# or Turn of the Luck; An Omen is called. 
# The mechanic works like this: one light D-10 for YES, one Dark D-10 for NO
# The die that 'loses' gets a Rank card chosen as a prompt.

import random

from oracle_data import RANKS

_omen_count = 0
_goal_completed = False

def _die_to_rank(value: int) -> str:
    if value == 1:
        return "A"
    if value == 0:
        return "10"
    return str(value)

# After a grounding lands (per the prompt in prompts.py), Claude reaches for this function when it determines that the goal has been reached during play.
def complete_goal() -> None:
    """Change goal_completed to True"""
    global _goal_completed
    _goal_completed = True

def cast_omen(hope: str) -> dict:
    """Cast an omen: roll two d10 (light and dark), compare — never sum — and read the result."""
    global _omen_count

    light = random.randint(0, 9)
    dark = random.randint(0, 9)

    if light == dark:
        return {
            "hope": hope,
            "light": light,
            "dark": dark,
            "doubles": True,
            "reading": "no answer — fate ate the question; the hand is called",
        }

    _omen_count += 1
    grounds_by = "player" if _omen_count % 2 == 1 else "claude"

    if light > dark:
        direction = "light"
        winner, loser = light, dark
    else:
        direction = "dark"
        winner, loser = dark, light

    gap = winner - loser
    if gap <= 3:
        texture = "...but (a complication rides in)"
    elif gap <= 6:
        texture = "clean"
    else:
        texture = "...and (better than asked, or worse than feared)"

    complication_rank = _die_to_rank(loser)

    return {
        "hope": hope,
        "light": light,
        "dark": dark,
        "doubles": False,
        "direction": direction,
        "gap": gap,
        "texture": texture,
        "complication_rank": complication_rank,
        "complication_meaning": RANKS[complication_rank],
        "grounds_by": grounds_by,
    }
