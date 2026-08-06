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

### Why persistence and the Journal got cut (2026-08-06) — outline for later

Working name for the axis this incident is really about: **generative vs.
classical code**, and why MCP doesn't give you a clean way to fold the two
together — especially inside Claude Desktop specifically, not just at the
protocol level. Persistence and the Journal of Fate are gone from the
codebase now (`persistence.py`, `journal_of_fate.py`, `reset_game`,
`save_game`, `log_journal_entry` all removed); this is the reasoning trail,
kept as an outline rather than finished prose, for whenever the article
gets written.

**The concrete incident, in order:**

- The new-Sitting overwrite guard (`sitting()` in `prompts.py`) was
  classical code — a plain `if thesitting.CHARACTER_NAME is not None`
  check — trying to hand off to the generative side with an instruction:
  "call `reset_game()`, then run the `/sitting` prompt again." That's not
  a real capability. Prompts are pull-only by MCP's own design (the
  session-2 finding, resurfacing here in a new shape) — a human has to
  invoke one, Claude structurally cannot. The classical code wrote a
  stage direction for an actor who doesn't have that move.
- Claude, unable to comply, substituted its own equivalent: called
  `name_character`/`draw_cross_card` directly, since those *are* tools it
  has autonomy over. But that path has no access to the ceremony text
  (the verbatim card recitation, the ordered WHERE-question gating) that
  only exists inside `sitting()`'s returned message — and no memory of
  the suit arguments the player had actually typed into the chip, since
  the guard's early return discarded them before they were ever used.
  Live result: a paraphrased, un-ceremonial cross, drawn from suits the
  player never chose.
- A second, independent wrinkle, specific to the client rather than the
  protocol: Claude Desktop rendered the prompt's own returned content as
  an untrusted file attachment, and on the confirmed-reset path, Claude's
  own safety layer explicitly labeled it "a potential injection attempt"
  before asking clarifying questions — because the content was
  instructing an irreversible action from inside something structurally
  identical to a file upload. Three independently reasonable layers
  (MCP's prompt-authority model, Desktop's attachment rendering, the
  model's own distrust of file-borne destructive instructions) stacked
  into a dead end none of the three "caused" alone.

**The reframe, not a patch:** the fix that was seriously considered
first — a new tool that resets, redraws, and recites atomically in one
autonomous call — would have worked, but only by giving up the very thing
that made a fresh Sitting feel ceremonial (or by duplicating the ritual
logic that already exists elsewhere in the file, which is its own kind of
bug waiting to happen). Instead of engineering a bridge across the seam,
the actual move was asking whether the feature *needing* the bridge was
worth it. It wasn't: persistence only ever saved structured state (cross,
debts, deck) — never the actual prose, voice, or established narrative
texture of a paused session. "Resuming a story" was never going to feel
seamless off that alone, so the thinner, real win (not losing a character
sheet) wasn't worth what it kept costing to defend. Cutting it dissolved
the underlying problem rather than solving it. The Journal of Fate went
for the identical reason, one level down — its whole docstring-stated
purpose ("the thing to check continuity against... a missed thread can't
be recovered later") was bridging a gap that no longer exists once a
session is meant to live entirely inside one continuous conversation.

**The general claim, for the article:** MCP's three primitives already
split cleanly along one axis — model-controlled (tools) vs.
human-controlled (resources, prompts). That axis is fine as long as
each feature stays on one side of it. The trouble shows up when a single
feature needs a human-controlled action (re-running a prompt) to happen
as an automatic *consequence* of something the model just decided
mid-conversation (confirming a destructive reset) — that need sits
exactly on the seam, and nothing in the primitive set is built to cross
it automatically. Every fix available at that seam trades something away
(duplicated logic, lost ceremony, or — what actually happened here —
cutting the feature that needed the bridge in the first place). Worth
distinguishing explicitly from the session-2 finding: that one was about
*which* primitive to pick for a given feature; this one is about a single
primitive trying to reach across the agency line from the inside, which
structurally can't be done no matter which primitive it is.

### Passive vs. active GM instructions — a pacing fix, for the article (2026-08-06)

First live playtest of the session-6 Unclaimed/scene-close redesign (built
since, never confirmed working until this session). The core mechanics
fired correctly — cold-read-then-ground on the Unclaimed, the compound
close condition, the reopening sequence all matched spec exactly. But one
scene (arriving at a gate, queuing, a conversation with an NPC and a
centaur, two full omens resolving) never closed at all — it just kept
running.

**Diagnosis:** not a bug. The scene's Unclaimed content ("a death kept
quiet") genuinely never landed in the fiction during that stretch, so one
of the two required close conditions was correctly never satisfied. The
instruction already had an escape hatch — "you can also flip the Unclaimed
again mid-scene, any time something genuinely new needs material" — but
it's phrased as a rare, permissive option, not something Claude reached
for even once despite several good openings in that same stretch.

**The general point worth writing up:** an instruction can be mechanically
correct and still produce bad pacing, because *correct* and *proactive*
aren't the same thing. The fix wasn't a new rule — it was rewriting an
existing, passive "you may, if you want" clause into an active "this is
your job as GM, reach for it" one, plus resolving a real ambiguity
underneath it (does a mid-scene Unclaimed flip's content count toward the
close, or only the one that opened the scene? — decided: whichever is
currently live, otherwise there'd be no payoff for using the escape hatch
at all).

**Current wording (`prompts.py`, scene-close paragraph):**

> A scene closes once two things are both true: the Unclaimed's grounded
> possibility has actually landed in the fiction, and an omen has been
> asked and resolved. Once both are true, name the close out loud — say
> plainly what closed it — then ask WHERE again and flip a fresh Unclaimed
> to open the next scene. You can also flip the Unclaimed again mid-scene,
> any time something genuinely new needs material rather than a
> yes-or-no answer.

**Proposed/shipped wording:**

> A scene closes once two things are both true: the currently live
> Unclaimed's grounded possibility has actually landed in the fiction, and
> an omen has been asked and resolved. Once both are true, name the close
> out loud — say plainly what closed it — then ask WHERE again and flip a
> fresh Unclaimed to open the next scene. Don't just wait for the current
> Unclaimed to land on its own — if an omen has already resolved in this
> scene and the Unclaimed's content still hasn't found its way in, that's
> your cue to actively steer the story toward it, or flip a fresh Unclaimed
> if the old one isn't pulling its weight. You're running this scene, not
> just adjudicating it: reach for the Unclaimed to keep things moving
> toward a close, not only when things go quiet.

Not yet playtested — next live session should confirm whether this
actually tightens scene length, or whether Claude still under-uses the
mid-scene flip even with more assertive wording.
