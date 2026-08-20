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
def complete_goal() -> dict:
    """Mark the current Sitting's Goal as completed, once the story has actually resolved it.

    Call at most once per Sitting, only after an Omen's grounding has landed
    and, checked against the Goal's saved interpretation (get_sheet's 'goal'
    field), genuinely resolves what the Goal meant — never call this
    preemptively, ahead of the grounding that earns it. Distinct from
    draw_goal_card, which deals the Goal at the start of the Sitting;
    complete_goal only marks it finished later in play.

    Takes no parameters. Idempotent in effect (repeated calls leave the flag
    True) but should only be invoked the one time the resolution actually
    happens. Sets and returns goal_completed as True.
    """
    global _goal_completed
    _goal_completed = True
    return {"goal_completed": _goal_completed}

def cast_omen(hope: str) -> dict:
    """Cast an omen: roll two ten-sided dice (light vs dark, compared not summed) to answer a real yes/no question with real stakes.

    Call whenever a scene reaches something no one can know in advance —
    other hearts, hidden things, or the turn of luck — or when a player
    claims an uncertain, high-stakes action simply succeeded. At least one
    omen must be asked before a scene can close. Not for material that just
    needs new story content rather than a yes/no answer — use
    draw_unclaimed_card for that instead.

    hope: a plain sentence naming the real stakes being asked about — what
    the asker hopes is true (e.g. "I hope the guard doesn't notice me").

    Not idempotent: each call rolls fresh dice and increments an internal
    counter that alternates who narrates the result. Doesn't mutate any
    other game state. Returns a dict describing the roll: on doubles,
    {hope, light, dark, doubles: True, reading} — no answer, the Hand is
    called instead (see call_the_hand). Otherwise {hope, light, dark,
    doubles: False, direction, gap, texture, complication_rank,
    complication_meaning, grounds_by} — direction and gap give the answer's
    shape, grounds_by says whether the player or Claude narrates the
    complication.
    """
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
