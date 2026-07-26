SUITS = {
    "♥": {"name": "Hearts", "domain": "love, loyalty, bonds"},
    "♦": {"name": "Diamonds", "domain": "wealth, desire, ambition"},
    "♣": {"name": "Clubs", "domain": "labor, craft, growth"},
    "♠": {"name": "Spades", "domain": "death, conflict, endings"},
}

RANKS = {
    "A": "a beginning; the seed; the suit in its purest form",
    "2": "a meeting; a pairing; a choice between two",
    "3": "growth; a first fruit; something spreading",
    "4": "stability; a holding; walls",
    "5": "a wound; loss; unbalance",
    "6": "a debt; an exchange; something owed",
    "7": "a secret; something hidden, or found",
    "8": "a toll; momentum; what must be paid to pass",
    "9": "the brink; almost; the edge",
    "10": "culmination; the full weight; nothing after this",
    "J": "a person: young, unproven; a messenger",
    "Q": "a person: quiet power; a keeper",
    "K": "a person: authority; one who commands the domain",
}

# Each tuple is (Hearts, Diamonds, Clubs, Spades) phrases for that rank.
_PHRASES_BY_RANK = {
    "A": ("the first thread of a lasting bond", "the first coin of a great sum", "work begun with bare hands", "an ending takes its first breath"),
    "2": ("a stranger who will not stay a stranger", "two prizes, one purse", "a task that needs four hands", "a parting of ways"),
    "3": ("the circle around your fire widens", "one coin becomes three", "the first fruit of long labor", "a small rot spreads"),
    "4": ("a door held open for you", "a hoard behind thick walls", "what you build here will stand", "a grave holds what it is given"),
    "5": ("a harsh word that cannot be unsaid", "something craved and lost", "the tool breaks in your hand", "the blade finds a gap"),
    "6": ("an old debt of kindness", "a debt come due", "hands owed to another's harvest", "blood asks for blood"),
    "7": ("a heart with a locked room", "a want no one admits", "the plough turns up more than soil", "a death kept quiet"),
    "8": ("no crossing without a goodbye", "the price of passage", "the work will not wait", "the water keeps what it is owed"),
    "9": ("one thread holds the whole bond", "fingers brush the gold", "the keystone waits", "one breath from the dark"),
    "10": ("nothing left to weave", "the great sum, counted", "the hands may rest at last", "the last breath"),
    "J": ("a messenger carrying more than the message", "a runner with a rich man's errand", "an apprentice with untried hands", "a youth with a borrowed sword"),
    "Q": ("the one who holds every thread", "the one who keeps the keys", "a keeper of the old ways", "a keeper of deaths"),
    "K": ("the one loved past reason", "the one who sets the price", "the master of a hundred hands", "the one death answers to"),
}

_SUIT_ORDER = ["♥", "♦", "♣", "♠"]

ORACLE_GRID = [
    {
        "rank": rank,
        "suit": suit,
        "suit_name": SUITS[suit]["name"],
        "domain": SUITS[suit]["domain"],
        "rank_meaning": RANKS[rank],
        "phrase": phrase,
    }
    for rank, phrases in _PHRASES_BY_RANK.items()
    for suit, phrase in zip(_SUIT_ORDER, phrases)
]
