from mcp.server.fastmcp import FastMCP

from oracle_data import ORACLE_GRID
from thesitting import draw_cross_card, draw_goal_card, name_character
from omens import cast_omen
from debt import call_the_hand
from defiance import defy_roll, defy_resolve
from sheet import get_sheet
from prompts import sitting

mcp = FastMCP("fortuneteller")


@mcp.resource("oracle://grid", mime_type="application/json")
def oracle_grid() -> list[dict]:
    """The Oracle Grid: all 52 fortune-phrases, with rank and suit meanings."""
    return ORACLE_GRID


mcp.resource("player://{player_name}/sheet", mime_type="application/json")(get_sheet)

mcp.prompt()(sitting)

mcp.add_tool(draw_cross_card)
mcp.add_tool(draw_goal_card)
mcp.add_tool(name_character)
mcp.add_tool(cast_omen)
mcp.add_tool(call_the_hand)
mcp.add_tool(defy_roll)
mcp.add_tool(defy_resolve)
mcp.add_tool(get_sheet)


if __name__ == "__main__":
    mcp.run()
