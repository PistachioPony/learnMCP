# The Fortuneteller's Hand — a Companion, and an MCP Server

An MCP server that acts as a mechanical companion and game master for **The
Fortuneteller's Hand**, an original solo tabletop RPG. Claude reads the
cards, casts the omens, and runs the table; the player just plays.

## What playing feels like

A short version, before you install anything: you sit with the
Fortuneteller first — where you meet them is the one choice made before any
card is drawn. Four suits become four facets of who you are; the
Fortuneteller draws one card from each and speaks what it reveals, and you
build a character from those four phrases. One more card — your Goal — and
you set out.

From there, every scene works the same way: decide where you are, flip a
card to see what's stirring, narrate forward. The moment the story reaches
another heart, something hidden, or needs a turn of luck, you stop and ask
fate directly — an Omen, not a guess. Fate can turn against you, too; when
it does, you can fight it.

This is, at heart, a creative journaling game. The real pleasure is in the
narration you and the Fortuneteller build together, not in winning
anything. Motivation, Ends, Seek, and Carry aren't rules to obey; they're
seeds, four starting points for your character's psychology and the shape
of the story ahead. Follow them where they lead, or let the story wander
somewhere else. The more you describe, the more the story gives back.

That's the shape of it. Full mechanics in [`RULES.md`](RULES.md); a
gentler, fuller walkthrough in [`HOW_TO_PLAY.md`](HOW_TO_PLAY.md). If you
ever lose track of your Goal or your four facets partway through a story,
just ask the Fortuneteller to remind you.

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

## Influences

This project draws from a few places. The Omens' two-dice reading, comparing
rather than summing, owes a real debt to *Ironsworn* by Shawn Tomkin. The
Defiance ritual, "Not Like This," borrows its five-dice, three-roll,
keep-what-you-want shape from Yahtzee. As a journaling game, this owes a lot
to *Thousand Year Old Vampire* by Tim Hutchings, one of the games that
proved solo, prompt-driven play could carry real weight. And the writing of
Max Moon has shaped the tone of this project throughout.

## Curious about the build?

This started as a way to learn the Model Context Protocol properly — the
tool/resource/prompt choices, the state design, a few real bugs found and
fixed along the way — all written up in [`DESIGN.md`](DESIGN.md). Or just
reach out to me directly.
