from typing import Literal

from mcp.server.fastmcp.prompts.base import UserMessage

import thesitting
from oracle_data import SUITS
from thesitting import draw_cross_card, draw_goal_card, name_character

_LENS_ORDER = ["Motivation", "Seek", "Ends", "Carry"]

_SUIT_NAME_TO_SYMBOL = {info["name"]: symbol for symbol, info in SUITS.items()}


def sitting(
    player_name: str,
    motivation_suit: Literal["Hearts", "Diamonds", "Clubs", "Spades"],
    ends_suit: Literal["Hearts", "Diamonds", "Clubs", "Spades"],
    seek_suit: Literal["Hearts", "Diamonds", "Clubs", "Spades"],
    carry_suit: Literal["Hearts", "Diamonds", "Clubs", "Spades"],
) -> UserMessage:
    """Run the Sitting: name the character, draw the cross, deal the Goal, and hand the moment to the player."""
    name_character(player_name)
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[motivation_suit], "Motivation")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[ends_suit], "Ends")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[seek_suit], "Seek")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[carry_suit], "Carry")
    draw_goal_card()

    lines = [
        f"The Sitting is done, {player_name}. Read these five lines to the "
        "player exactly as written — don't paraphrase or summarize them:"
    ]
    for position in _LENS_ORDER:
        card = thesitting.CROSS[position]
        lines.append(f"**{position} — {card['suit_name']}.** *{card['phrase']}*")
    goal = thesitting.GOAL
    lines.append(f"**The Goal — {goal['suit_name']}.** *{goal['phrase']}*")

    lines.append(
        "\nTell me about your character — who these four phrases describe — "
        "and what your Goal means to them, in their own words."
    )

    lines.append(
        "\nFrom here, narrate the story forward, but the player authors their own "
        "character's words, choices, and actions — that's theirs, don't take it from "
        "them. Watch instead for the moment their narration reaches into one of fate's "
        "three withheld domains: other hearts (anything with its own will — what someone "
        "else decides, feels, or does), hidden things (what's hidden, behind, beneath, or "
        "not yet arrived), or the turn of luck. The instant their narration leans on one "
        "of those, stop before answering it yourself and tell them: an omen must be "
        "called. When an omen resolves, report its raw shape first — direction, gap, and "
        "any complication rank — before you say what it means; then stop and let the "
        "player ground the reading in their own words, and only pick up narrating once "
        "they have. If an omen comes back doubles, call the hand yourself immediately — "
        "that part isn't the player's to invoke. If a fortune lands and they want to "
        "fight it, tell them to call defiance."
    )

    lines.append(
        "\nAt any point, the player may say \"read it truer\" if your narration "
        "betrays a card's domain, magnitude, or phrase — suit is domain, rank is "
        "magnitude, the phrase is flavor. Don't defend the read: just narrate it "
        "again, truer."
    )

    return UserMessage("\n\n".join(lines))
