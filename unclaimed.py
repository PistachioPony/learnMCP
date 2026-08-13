# This module is used to draw from "The Unclaimed" Deck
# It is the same deck as the Fortuneteller's Hand
# but we need to call it something different because of the 
# way MCP tools work. In Prompts.py I have told Claude that
# it needs to watch for a few different instances when it 
# needs to flip a card and what to do with it. 
# I chose to create a separate module for each tool's function.
# to keep it visually clean and understandable.  

from hand_deck import draw_from_hand_deck


def draw_unclaimed_card() -> dict:
    """Flip a card from the Fortuneteller's Hand for the Unclaimed: read cold, before any narration."""
    return draw_from_hand_deck()
