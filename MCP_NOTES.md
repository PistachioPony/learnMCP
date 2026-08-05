# MCP Notes

Working notes on MCP itself (the protocol, the primitives) and on what makes
this project interesting as an MCP project, not just as a game. Add to this
as things come up.

## Sources to read later

On prompts orchestrating tools / workflow prompts — the pattern behind
`prompts.py`'s `sitting()`, which both calls tool functions directly as
setup *and* returns a message that primes Claude to call other tools
autonomously later in the conversation:

- [MCP Prompts and Resources: The Primitives You're Not Using](https://dev.to/aws-heroes/mcp-prompts-and-resources-the-primitives-youre-not-using-3oo1)
- [MCP resources vs tools vs prompts: when to use each · Stacktree](https://stacktr.ee/blog/mcp-resources-vs-tools-vs-prompts)
- [Prompts - Model Context Protocol (official spec)](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
- [MCP Series: Adding Prompts in an MCP Server — Templating Interactions for Consistency](https://medium.com/@whatsupai/mcp-series-prompts-in-mcp-templating-interactions-for-consistency-5858f23b8882)

## What's interesting about this project as an MCP project

Started 2026-08-04. Notes so far:

- The `sitting()` prompt combines two things most tutorial-level MCP
  examples do separately: direct server-side tool invocation (setup —
  naming the character, drawing the cross and Goal) and priming the model
  to invoke *other* tools autonomously later (`draw_unclaimed_card`,
  `log_journal_entry`, `save_game`) as play unfolds. Docs and blog posts
  describe "prompts orchestrating tools" as a real pattern, but the
  specific stitch of setup-now + prime-for-later wasn't something the
  research turned up as an already-named or widely-illustrated recipe —
  most examples do one half or the other.
- Worth digging into further: is this combination worth naming/describing
  explicitly when presenting the project? It may be the most technically
  interesting design decision in the codebase, separate from the game
  content itself.

### Cards + dice, not cards-only

Corrected an earlier claim: this project isn't card-only. Omens run on two
d10s (compared, not summed — `omens.py`) and Defiance runs on five d6s
(`RULES.md`). Dice and cards do different jobs: **dice decide the shape of
an answer** (whether fate answers at all, how sharp the outcome is, whether
a complication rides in); **cards supply the content** (fixed domain via
suit, magnitude via rank, flavor via phrase) that narration has to honor.
Most dice-based RPG-MCP servers found so far (see below) use dice for both
resolution and content — this project splits that job across two separate
systems. That split, not "no dice," is the accurate distinguishing claim.

Also worth being precise about: Claude *does* improvise constantly during
play — narration itself is improvisation. What's fixed is only three axes
per card (suit/rank/phrase = domain/magnitude/flavor); "read it truer"
enforces staying faithful to those axes, not a ban on improvising. Omens
have a stricter, temporary rule: Claude states only the raw mechanical
shape and stops, letting the player ground the meaning first — but that's
a sequencing rule, not a permanent lock on improvisation.

### Comparison: dmcp (shawnrushefsky) vs. this project

[dmcp](https://github.com/shawnrushefsky/dmcp) is the closest match found
among MCP "AI dungeon master" servers — TypeScript, SQLite-backed, general
enough for any setting. Compared its narrative-logging tool
(`src/tools/narrative.ts`) directly against `journal_of_fate.py` +
`persistence.py`:

- **dmcp**: real event-sourced system. SQLite `narrative_events` table
  (id, gameId, open-ended `eventType` string, freeform `content`, arbitrary
  `metadata` JSON), full CRUD, filtered history queries (by type/time
  range/limit/offset), summary stats, realtime event emission over a
  pub/sub bus (feeds a live client UI). On top of that, `exportStoryData()`
  groups events into "chapters" by a day-change/major-event heuristic and
  can render the result in ten canned prose styles (noir, epic fantasy,
  screenplay, journal, etc.), each with a hardcoded style instruction.
- **This project**: one function, closed three-field schema (`name`,
  `kind` locked to person/place/thing via `Literal`, `note`), in-memory
  list, dumped wholesale as part of one flat JSON snapshot on `save_game()`.
  No query surface, no filtering, no chaptering, no export styles.

The real difference isn't "less code" — it's *where the interpretive labor
lives*. dmcp keeps the schema wide open and does interpretation in code,
after the fact (chaptering heuristics, style lookup tables), treating the
log as raw material a program reshapes into prose later. This project
keeps the schema narrow and puts the interpretive work in the docstring —
plain English instructing Claude what's worth logging and why — used live,
during play, trusting the model's judgment in the moment rather than
processing the log afterward.

Nameable axis for presenting the project: **structured event-sourcing +
post-hoc code-driven narrativization** (dmcp) vs. **minimal typed memory +
trust-the-model in-context judgment** (this project). Given the project's
ethos in `RULES.md` — restraint, "Claude-the-collaborator," fate keeping
things behind its hand — the minimal/trust-the-model choice reads as
deliberate, not unfinished.
