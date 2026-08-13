# When doubles are rolled from an Omen,
# this module takes care to read from a player's row of Debt cards 
# if they have one. If not, a card is flipped 
# from the Fortuneteller's Hand.

from hand_deck import draw_from_hand_deck

DEBT_ROW: list[dict] = []


def call_the_hand() -> dict:
    """Doubles trigger: play the table-wide ripest debt card, or deal a fresh card from the Fortuneteller's Hand deck if every row is clean."""
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
