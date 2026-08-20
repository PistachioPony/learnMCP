# This module can be seen as the character sheet. 
# it holds the Player's character name, drives, goal and
# debt row if they have one. 
# The word "Cross" is from the tabletop version of the game.

import thesitting
import debt
import omens


def get_sheet(player_name: str) -> dict:
    """Read the current character sheet: the Sitting's cross, Goal, debt row, and whether the Goal is completed.

    Call any time you need to check saved state rather than re-deriving
    it — for example, checking the Goal's saved interpretation before
    calling complete_goal, or checking goal_completed before deciding
    whether to close the campaign at a scene's end. Read-only: never
    mutates game state.

    player_name: must exactly match the name already set via
    name_character for the character currently in play; raises ValueError
    if no character has been named yet, or if the name doesn't match the
    current character.

    Returns a dict with cross (the four drive-to-card mapping), goal (the
    dealt Goal card plus its recorded interpretation, or None if not yet
    dealt), debt_row (list of outstanding debt cards), and goal_completed
    (bool).
    """
    if thesitting.CHARACTER_NAME is None:
        raise ValueError("No character has been named yet — call name_character first.")
    if player_name != thesitting.CHARACTER_NAME:
        raise ValueError(f"No character named '{player_name}' — the current character is '{thesitting.CHARACTER_NAME}'.")
    return {"cross": thesitting.CROSS, "goal": thesitting.GOAL, "debt_row": debt.DEBT_ROW, "goal_completed": omens._goal_completed}
