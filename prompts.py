from typing import Literal

from mcp.server.fastmcp.prompts.base import UserMessage

import thesitting
from thesitting import draw_cross_card, draw_goal_card, name_character

_LENS_ORDER = ["Motivation", "Seek", "Ends", "Carry"]


def sitting(
    player_name: str,
    motivation_suit: Literal["♥", "♦", "♣", "♠"],
    ends_suit: Literal["♥", "♦", "♣", "♠"],
    seek_suit: Literal["♥", "♦", "♣", "♠"],
    carry_suit: Literal["♥", "♦", "♣", "♠"],
) -> UserMessage:
    """Run the Sitting: name the character, draw the cross, deal the Goal, and hand the moment to the player."""
    name_character(player_name)
    draw_cross_card(motivation_suit, "Motivation")
    draw_cross_card(ends_suit, "Ends")
    draw_cross_card(seek_suit, "Seek")
    draw_cross_card(carry_suit, "Carry")
    draw_goal_card()

    lines = [f"The Sitting is done, {player_name}. The cards, in order:"]
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
        "called. If an omen comes back doubles, call the hand yourself immediately — that "
        "part isn't the player's to invoke. If a fortune lands and they want to fight it, "
        "tell them to call defiance."
    )

    return UserMessage("\n\n".join(lines))
