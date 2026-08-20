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
    """Draw one card from the Fortuneteller's Hand deck to open or refuel a scene with new story material.

    Call at the start of every new scene, and again mid-scene any time the
    story genuinely needs new material rather than a yes/no answer — for a
    yes/no question, use cast_omen instead. Read the returned phrase cold,
    before narrating anything else; only afterward do you narrate the scene
    forward and let its meaning land in the fiction.

    Takes no parameters. Not idempotent: each call removes and returns a
    different card from the shared, shuffled deck (auto-reshuffles when the
    deck runs out). Returns a dict with rank, suit, suit_name, domain,
    rank_meaning, and phrase.
    """
    return draw_from_hand_deck()
