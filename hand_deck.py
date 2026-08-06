import random

from oracle_data import ORACLE_GRID


# the Fortuneteller's Hand deck, freshly shuffled at module load.
HAND_DECK = random.sample(ORACLE_GRID, len(ORACLE_GRID))


def draw_from_hand_deck() -> dict:
    """Draw the top card of the Fortuneteller's Hand deck. If it's run dry, reshuffle in every card that isn't currently outstanding debt."""
    global HAND_DECK
    if not HAND_DECK:
        import debt

        owed = {(c["rank"], c["suit"]) for c in debt.DEBT_ROW}
        HAND_DECK = [c for c in ORACLE_GRID if (c["rank"], c["suit"]) not in owed]
        random.shuffle(HAND_DECK)
    return HAND_DECK.pop()
