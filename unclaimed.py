from hand_deck import draw_from_hand_deck


def draw_unclaimed_card() -> dict:
    """Flip a card from the Fortuneteller's Hand for the Unclaimed: read cold, before any narration."""
    return draw_from_hand_deck()
