# When doubles are rolled from an Omen,
# this module takes care to read from a player's row of Debt cards 
# if they have one. If not, a card is flipped 
# from the Fortuneteller's Hand.

from hand_deck import draw_from_hand_deck

DEBT_ROW: list[dict] = []


def call_the_hand() -> dict:
    """Trigger the Called Hand: an omen rolled doubles, so fate intrudes on the scene instead of answering the question.

    Call immediately whenever cast_omen returns doubles=True — this isn't
    the player's to invoke, Claude always calls it. Plays the oldest
    outstanding debt card if any are owed (owed debt always comes due
    first), otherwise deals a fresh card from the Fortuneteller's Hand
    deck. Either way the landing must intrude on the scene — it costs
    something, and the original question the omen asked stays unanswered.
    If the player wants to fight the landed fortune, that's when they call
    defiance (see defy_roll).

    Takes no parameters. Not idempotent: mutates the shared debt row
    (pops the oldest card) or the shared Hand deck (deals a fresh card).
    Returns a dict with source ("debt_row" or "fresh_deal"), card (the
    landed card's rank/suit/phrase/etc.), and a fixed note reminding you
    the landing must intrude and the question stays unanswered.
    """
    if DEBT_ROW:
        card = DEBT_ROW.pop(0)
        source = "debt_row"
    else:
        card = draw_from_hand_deck()
        source = "fresh_deal"

    return {
        "source": source,
        "card": card,
        "note": "The landing must intrude — it costs the scene. The question you asked stays unanswered.",
    }
