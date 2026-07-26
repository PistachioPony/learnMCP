from mcp.server.fastmcp import FastMCP

from oracle_data import ORACLE_GRID
from thesitting import draw_cross_card
from omens import cast_omen
from debt import call_the_hand
from defiance import defy_roll, defy_resolve

mcp = FastMCP("fortuneteller")


@mcp.resource("oracle://grid")
def oracle_grid() -> list[dict]:
    """The Oracle Grid: all 52 fortune-phrases, with rank and suit meanings."""
    return ORACLE_GRID


mcp.add_tool(draw_cross_card)
mcp.add_tool(cast_omen)
mcp.add_tool(call_the_hand)
mcp.add_tool(defy_roll)
mcp.add_tool(defy_resolve)


if __name__ == "__main__":
    mcp.run()
