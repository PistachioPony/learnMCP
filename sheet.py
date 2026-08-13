# This module can be seen as the character sheet. 
# it holds the Player's character name, drives, goal and
# debt row if they have one. 
# The word "Cross" is from the tabletop version of the game.

import thesitting
import debt
import omens


def get_sheet(player_name: str) -> dict:
    """A player's current cross and debt row."""
    if thesitting.CHARACTER_NAME is None:
        raise ValueError("No character has been named yet — call name_character first.")
    if player_name != thesitting.CHARACTER_NAME:
        raise ValueError(f"No character named '{player_name}' — the current character is '{thesitting.CHARACTER_NAME}'.")
    return {"cross": thesitting.CROSS, "goal": thesitting.GOAL, "debt_row": debt.DEBT_ROW, "goal_completed": omens._goal_completed}
