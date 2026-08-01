# The Fortuneteller's Hand — a Companion, and an MCP Server

An MCP server that acts as a mechanical companion and game master for **The
Fortuneteller's Hand**, an original solo tabletop RPG. Claude reads the
cards, casts the omens, and runs the table; the player just plays.

This project started as a way to learn the Model Context Protocol properly —
not with a toy demo, but by building against a real game with a real
economy, real state, and real consequences for getting the state wrong.

## Why this is technically interesting

- **Tool vs. resource placement is based on tested behavior, not
  assumption.** Resources in MCP are pull-only — a human has to deliberately
  fetch them; a model can't reach for one autonomously mid-conversation. That
  distinction isn't obvious from the spec alone, and this project found it by
  testing live: a resource that worked in isolation silently failed the
  moment the model needed to check it on its own. The fix was to register
  the same underlying function twice — once as a resource, once as a tool —
  based on who actually needs to initiate the read. See `sheet.py` +
  `main.py`.

- **A prompt does real orchestration, not just templating.** The `sitting`
  prompt (`prompts.py`) runs deterministic Python — naming the character,
  drawing all four cross cards, dealing the Goal — before it ever returns a
  message. That's a deliberate choice not to trust the model to chain five
  tool calls in the right order; the prompt *is* the orchestration.

- **State carries real invariants, not just values.** Two independent
  52-card decks (one committed entirely at character creation, one drawn
  from throughout play), a debt-row economy, and a reshuffle mechanic that
  has to reason about what's currently owed — a card can't be reshuffled
  back into play while its debt twin is still outstanding, or the same
  fortune could land twice. See `hand_deck.py`'s `draw_from_hand_deck()`.

## Architecture at a glance

| File | MCP primitive(s) | Responsibility |
|---|---|---|
| `main.py` | — | Thin registration layer; the only file that touches the `mcp` server object |
| `oracle_data.py` | resource (`oracle://grid`) | The fixed 52-phrase reference grid |
| `thesitting.py` | tools | Character creation: the cross, the Goal, Fate's deck |
| `hand_deck.py` | (shared infra) | The Fortuneteller's Hand deck, with Told/reshuffle logic |
| `omens.py` | tool | The compare-never-sum omen resolution, stateless |
| `debt.py` | tool | The debt row and the Called Hand |
| `defiance.py` | tool | The multi-roll defiance ritual |
| `unclaimed.py` | tool | The Unclaimed: a turn's content-generation beat |
| `sheet.py` | resource + tool | The player's cross/debt sheet — registered as both, deliberately |
| `prompts.py` | prompt | The Sitting ritual and the standing GM instruction |

Every file above `main.py` is plain Python with no MCP dependency of its own
— it can be read, tested, and understood on its own terms. MCP is the
delivery layer wrapped around it, not the logic itself.

## Running it

Requires Python and [`uv`](https://docs.astral.sh/uv/).

1. `uv sync` inside this directory.
2. In Claude Desktop: Settings → Developer → Edit Config, and add:
   ```json
   {
     "mcpServers": {
       "fortuneteller": {
         "command": "uv",
         "args": ["run", "--directory", "/absolute/path/to/learnMCP", "main.py"]
       }
     }
   }
   ```
3. Fully quit and restart Claude Desktop.
4. Click the `+` icon near the message box → Connectors → enable
   "fortuneteller."
5. Start a new chat and pull in the `sitting` prompt.

## Further reading

- [`RULES.md`](RULES.md) — the full solo ruleset: the Sitting, the Turn,
  Omens, the Called Hand, Defiance.
- [`DESIGN.md`](DESIGN.md) — the reasoning behind the decisions above, in
  more depth.
