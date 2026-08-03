from typing import Literal

JOURNAL: list[dict] = []


def log_journal_entry(name: str, kind: Literal["person", "place", "thing"], note: str) -> dict:
    """Log a new significant person, place, or thing to the Journal of Fate. `note` should be a brief, specific fact worth remembering later — the thing to check continuity against, not a full description."""
    entry = {"name": name, "kind": kind, "note": note}
    JOURNAL.append(entry)
    return entry
