# Design Notes

The reasoning behind the decisions in this project — what the options were,
what got chosen, and why. Game flavor is kept light here deliberately; this
is about the engineering, not the lore.

## Why this domain, not a toy oracle demo

The first pitch was a generic tarot/oracle draw-a-card toy. That got dropped
once it was clear that The Fortuneteller's Hand — a TTRPG project I am currently working on, seemed to map onto MCP's three primitives quite easily: the 52 fortune-phrases as a natural
**resource**, card draws and dice rituals as natural **tools**, the fixed
ritual language as a natural **prompt**. More importantly, the game's
debt-row economy forced real cross-call **state** — a harder and more
honest problem than a stateless dice roller would have offered.

## Lesson 1: resources are pull-only

A `player://{player_name}/sheet` resource template was built and worked in
isolation. Then, in live use, asking in plain language to "show the sheet"
completely failed. Claude reconstructed an answer from memory rather than
reading the resource at all. Resources are designed to be pulled by a human, explicitly. Seen by the user as a `+` menu pick
in Claude Desktop, or an `@`-mention in Claude Code. There is no path for the
model to decide, mid-conversation, to go check one on its own. (The protocol
itself doesn't strictly forbid a client from wiring up model-driven resource
selection, but neither client tested here does.)

The fix: register the same underlying function twice — once as a resource,
for deliberate human pull, once as a tool, for the model's own autonomous
use. One source of truth, two registrations, chosen by asking who actually
needs to initiate the read.

```python
# main.py
mcp.resource("player://{player_name}/sheet", mime_type="application/json")(get_sheet)
...
mcp.add_tool(get_sheet)
```

## Lesson 2: a prompt can just run code

An MCP prompt handler is plain Python, free to call other functions
directly before it ever returns a message. Rather than hoping the model
would correctly chain five tool calls in the right order (name the
character, draw four cross cards, deal the Goal), `sitting()` calls them
directly and deterministically, then returns one assembled message.

That message isn't static either. An early version revealed a real fidelity
bug: it dealt all five cards in one shot before ever asking who the
character was and checked against the game's own canon, this broke the
intended order, which was: meet the Fortuneteller → reveal the cards drawn for the 'drives' (called 'The Cross' in my Real Life version of the game) → describe the
character → *then* reveal the Goal). The fix turned the single returned
message into a staged script, with explicit "once they've answered X" gates
for each beat. The card *drawing* stays deterministic in code; only reveal
*timing* is staged through instructions, since a prompt returns exactly once
but the conversation keeps going in ordinary turns after that.

## Lesson 3: two independent decks, not one shuffled pool

Fate's deck (`thesitting.py`'s `SUIT_PILES`) is used entirely during the
'Sitting' itself. The four 'Drives' draws and the Goal deal use that deck and are never touched
again once character creation is done. The Fortuneteller's Hand
(`hand_deck.py`) is a second, fully independent 52-card deck used for
everything else during play: the Unclaimed's content-generation beat, the
Called Hand's landings, and the fresh debt cards that 'Defiance' deals.

A simpler version was on the table early on: draw four random cards from
one shared 52-card pool instead of maintaining four separate suit piles.
Same implementation effort either way, but the simpler version would have
silently broken the actual design intent: a guaranteed one-suit-per-position
cross with no duplicate domains. Once that was surfaced, the real mechanic
stayed.

## Lesson 4: a reshuffle has to reason about what's still owed

The Hand deck feeds two different mechanics: the Unclaimed, which reads a
card immediately, and the Called Hand, which either resolves outstanding
debt or deals a fresh card that can itself become debt through defiance. When
the live deck runs dry, it has to reshuffle — but a card currently sitting
in the debt row has been drawn and is outstanding, not spent. Reshuffling it
back into play risks the same fortune landing twice while its debt twin is
still owed.

Resolved without any new tracked state: the recyclable pool, at reshuffle
time, is simply the full 52-card set minus whatever's currently in the debt
row — derived on the spot, not bookkept separately.

```python
def draw_from_hand_deck() -> dict:
    global HAND_DECK
    if not HAND_DECK:
        import debt
        owed = {(c["rank"], c["suit"]) for c in debt.DEBT_ROW}
        HAND_DECK = [c for c in ORACLE_GRID if (c["rank"], c["suit"]) not in owed]
        random.shuffle(HAND_DECK)
    return HAND_DECK.pop()
```

## The process: found live, fixed at the root, not patched over

A few representative examples, not the full log:

- **A silent client-side validation failure.** Claude Desktop sent
  malformed suit values that failed a strict type check, and the client
  only reported a generic "failed to attach prompt" with no detail. The
  actual cause, found in Claude Desktop's own per-server log file, was
  that MCP's `PromptArgument` never sends enum information to the client at
  all, so the client had nothing to validate against, and nothing useful to
  show the user. Fixed by accepting plain names and translating internally,
  since prompt arguments are filled in by a human, not the model.

- **A ritual sequencing bug, caught by playing cold.** An early version of
  the Sitting dealt all five cards in one shot before ever asking who the
  character was. Found because a fresh playtester, without the rules open,
  independently narrated what she expected the ritual's order to be, and
  it didn't match what the code actually did. Checked against canon,
  confirmed as a genuine bug, fixed the same session.

- **A rule that only covered half the actors.** The standing instruction to
  watch for trespass into fate's withheld territory only ever mentioned the
  *player's* narration. A live session surfaced Claude inventing a hidden
  fact entirely on its own — an NPC's secret, decided with no dice at all.
  The actual rule applies to anyone's authorship, not just the player's;
  confirmed against the rules text and widened accordingly.

## What's still rough — an honest accounting

- **No persistence.** Every piece of game state — the cross, the Goal, the
  debt row, both card decks — lives in plain Python module-level variables
  inside the server process. Nothing is written to disk. Restarting the
  server is currently the only way to reset state, and there's no way to
  pause a session and genuinely resume it later.
- **Single-session architecture.** State is an implicit singleton, assuming
  exactly one character exists at a time. A real deployment would need
  actual session scoping.
- **No remote hosting.** The server runs over stdio, as a local subprocess
  launched by Claude Desktop or Claude Code — it requires Python, `uv`, and
  manual config-file editing to install. There's no version of this yet
  that someone non-technical could just click into.
- **Onboarding is undesigned.** Nothing in the running server explains
  itself to a first-time player; this document, Rules, How to Play and the Readme must be read before play to know how to use it.

None of this is an oversight so much as the honest next layer of work. I may even create a version playable through Slack.


