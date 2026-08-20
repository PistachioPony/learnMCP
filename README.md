# The Fortuneteller's Hand — an RPG MCP Server

An MCP server that acts as a role playing game and GM using the rules of **The
Fortuneteller's Hand**, an original tabletop RPG that I am currently working on. Claude reads the cards, casts the omens, and runs the table; the player and Claude will take turns narrating the story that develops. 

## What playing feels like

A short version, before you install anything: you sit with the
Fortuneteller first — where you meet them is the one choice made before any
card is drawn. Four suits become four facets of who you are; the
Fortuneteller draws one card from each and speaks what it reveals, and you
build a character from those four phrases. 
Once you have your character, you must interpret your Goal card before you set out.

From there, every scene works the same way: decide where you are, flip a
card to see what's stirring, narrate forward. The moment the story reaches
another heart, something hidden, or needs a turn of luck, you stop and ask
fate directly by calling an Omen. Fate can turn against you, too; when
it does, you can fight it.

This is, at heart, a creative journaling game. The real pleasure is in the
narration you and the Fortuneteller build together, not in winning
anything. Motivation, Ends, Seek, and Carry aren't rules to obey; they're
seeds, four starting points for your character's psychology and the shape
of the story ahead. Follow them where they lead, or let the story wander
somewhere else. The more you describe, the more the story gives back.

That's the shape of it. Full mechanics in [`RULES.md`](RULES.md); a
gentler, fuller walkthrough in [`HOW_TO_PLAY.md`](HOW_TO_PLAY.md); a full
transcript of an actual session in
[`08-2026-Play-Example.md`](08-2026-Play-Example.md). If you ever lose
track of your Goal or your four facets partway through a story, just ask
the Fortuneteller to remind you.

## Running it

### Quick install

1. Save [`learnMCP.mcpb`](learnMCP.mcpb) somewhere findable.
2. Double-click it (don't drag it into a chat window — just double-click
   the file itself). It'll open an install prompt in Claude Desktop.
3. Confirm the install.
4. Fully quit and reopen Claude Desktop.
5. Start a new chat, and pull in the `start_game` prompt — it'll ask for a
   character name, then you're off.

### Run from source

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
5. Start a new chat and pull in the `start_game` prompt.
6. When it asks for your character's name (`player_name`), fill that in.
7. Once the prompt attaches as a chip above the message box, click send or
   hit enter — attaching it doesn't submit it on its own.

## Influences

This project draws from a few places. The Omens' two-dice reading, comparing
rather than summing, owes a real debt to *Ironsworn* by Shawn Tomkin, which I absolutely LOVE. The
Defiance ritual, "Not Like This," borrows its five-dice, three-roll,
keep-what-you-want shape from Yahtzee (which was stolen from the Puerto Rican game "Jenerala"). As a journaling game, this owes a lot
to *Thousand Year Old Vampire* by Tim Hutchings, one of the games that
proved solo, prompt-driven play could carry real weight. Incredible game! And finally, Max Moon has shaped the tone of this project throughout. I adore everything Max Moon creates.

## Curious about the build?

This started as a way to learn the Model Context Protocol in a way that would interest me. The tool/resource/prompt choices, the state design, a few real bugs found and
fixed along the way, these are all written up in [`DESIGN.md`](DESIGN.md). If you have any questions or wish me to fix, or add anything, please contact me.

## Privacy Policy

- Data collection: This MCP collects nothing.
- Usage and storage: Nothing is stored. All game state (your character, cards drawn, debt owed) exists only in memory for the length of your session and is discarded when it ends.
- Third-party sharing: Nothing is shared with any third party, because nothing is collected in the first place.
- Data retention: Nothing is retained.
- Contact information: maria@mariasaha.com

