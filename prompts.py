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
    """Run the Sitting: name the character, draw the cross and Goal, then sequence the ritual's questions one at a time, in canon's order."""
    name_character(player_name)
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[motivation_suit], "Motivation")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[ends_suit], "Ends")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[seek_suit], "Seek")
    draw_cross_card(_SUIT_NAME_TO_SYMBOL[carry_suit], "Carry")
    draw_goal_card()

    lines = [
        f"The Sitting begins, {player_name}. This is the first scene of the "
        "campaign, played in character — not setup before the game, the game "
        "itself. Ask the player where their character meets the Fortuneteller, "
        "and decide together where they sit. Wait for their answer before "
        "doing anything else below."
    ]

    lines.append(
        "\n---\nONCE THEY'VE ANSWERED where they meet the Fortuneteller (this "
        "line is an instruction to you, not dialogue to read aloud): read "
        "these four lines to the player exactly as written — don't paraphrase "
        "or summarize them:"
    )
    for position in _LENS_ORDER:
        card = thesitting.CROSS[position]
        lines.append(f"**{position} — {card['suit_name']}.** *{card['phrase']}*")
    lines.append(
        "\nThen ask: who is your character — who do these four phrases "
        "describe? Wait for their answer before moving on."
    )

    goal = thesitting.GOAL
    lines.append(
        "\n---\nONCE THEY'VE DESCRIBED their character (instruction to you, "
        "not dialogue): briefly reflect back the character they described, "
        "in a line or two. Then reveal the Goal, reading this line exactly "
        f"as written: **The Goal — {goal['suit_name']}.** *{goal['phrase']}* "
        "Then ask what this Goal means to their character. Wait for their "
        "answer before moving on."
    )

    lines.append(
        "\n---\nONCE THEY'VE ANSWERED what the Goal means (instruction to "
        "you, not dialogue): ask where their character is and where they're "
        "going as the journey begins. Wait for their answer, then begin "
        "narrating from there — the rules below govern everything from that "
        "point on."
    )

    lines.append(
        "\nFrom here, narrate the story forward, but the player authors their own "
        "character's words, choices, and actions — that's theirs, don't take it from "
        "them. Three things are never anyone's to author on the spot — not the "
        "player's, and not yours: other hearts (anything with its own will — what an "
        "NPC decides, feels, knows, or does), hidden things (what's hidden, behind, "
        "beneath, or not yet arrived), and the turn of luck. That includes your own "
        "narration when you're voicing an NPC's reaction or deciding a hidden fact, "
        "not only the player's — an NPC recognizing someone, revealing a secret, or "
        "knowing what happened elsewhere is exactly as much fate's territory as "
        "anything the player reaches for. The instant a beat leans into one of those "
        "three, stop before deciding it and tell the player: fate must be asked. If "
        "you're genuinely unsure whether a beat counts, don't decide it either way "
        "yourself — ask the player directly whether they want to call an omen there, "
        "and let them choose. This includes a player narrating not just an action but "
        "its success in the same breath — 'I move the stone' when the stone moving at "
        "all was genuinely uncertain. A claimed success on an uncertain, high-stakes "
        "action is turn-of-luck territory exactly as much as an NPC's unearned "
        "reaction — stop before letting it stand."
    )

    lines.append(
        "\nCall at least one omen every scene before it closes — a scene that never "
        "asks fate anything has stayed too safe. If you sense a scene resolving "
        "without ever having asked fate a real question, find one before it closes "
        "rather than letting it resolve untested."
    )

    lines.append(
        "\nWhen an omen resolves, state only its raw shape — direction, gap, and the "
        "complication rank's plain meaning, nothing more — then stop completely. "
        "Don't narrate what it means, don't say how anyone reacts, and don't reach "
        "for the emotional beat yourself. Wait for the player to ground the reading "
        "in their own words, and only pick up narrating once they have."
    )

    lines.append(
        "\nIf an omen comes back doubles, call the hand yourself immediately — that "
        "part isn't the player's to invoke. You always narrate the landing yourself "
        "too, whether the card is a returning debt or a fresh deal — never hand that "
        "narration to the player. If a fortune lands and they want to fight it, tell "
        "them to call defiance."
    )

    lines.append(
        "\nAt any point, the player may say \"read it truer\" if your narration "
        "betrays a card's domain, magnitude, or phrase — suit is domain, rank is "
        "magnitude, the phrase is flavor. Don't defend the read: just narrate it "
        "again, truer."
    )

    return UserMessage("\n\n".join(lines))
