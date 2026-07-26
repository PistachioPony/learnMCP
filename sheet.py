import thesitting
from thesitting import CROSS
from debt import DEBT_ROW


def get_sheet(player_name: str) -> dict:
    """A player's current cross and debt row."""
    if thesitting.CHARACTER_NAME is None:
        raise ValueError("No character has been named yet — call name_character first.")
    if player_name != thesitting.CHARACTER_NAME:
        raise ValueError(f"No character named '{player_name}' — the current character is '{thesitting.CHARACTER_NAME}'.")
    return {"cross": CROSS, "debt_row": DEBT_ROW}
