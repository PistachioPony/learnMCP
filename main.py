# pulls in the official MCP SDK (the framework, not our own code).
# everything in this file tells the server what is available. 
from mcp.server.fastmcp import FastMCP

# pull in the my modules & its logic
from thesitting import draw_cross_card, draw_goal_card, name_character, record_goal_interpretation
from omens import cast_omen
from omens import complete_goal
from debt import call_the_hand
from defiance import defy_roll, defy_resolve
from unclaimed import draw_unclaimed_card
from sheet import get_sheet
from prompts import sitting

# instantiate the MCP - create the server object.
# shows up as connector name.
mcp = FastMCP("fortuneteller")

# RESOURCES = data a human deliberately pulls in.
# a resource template (takes in variables).
mcp.resource("player://{player_name}/sheet", mime_type="application/json")(get_sheet)

# registering the prompt we can invoke.
# PROMPTS = a fixed, reusable message template that
# a human explicitly invokes.
mcp.prompt()(sitting)

# registering the tools.
# TOOLS = things the model calls automnomously mid-conversation.
mcp.add_tool(draw_cross_card)
mcp.add_tool(draw_goal_card)
mcp.add_tool(name_character)
mcp.add_tool(record_goal_interpretation)
mcp.add_tool(cast_omen)
mcp.add_tool(call_the_hand)
mcp.add_tool(defy_roll)
mcp.add_tool(defy_resolve)
mcp.add_tool(draw_unclaimed_card)
mcp.add_tool(get_sheet)
mcp.add_tool(complete_goal)


if __name__ == "__main__":
    mcp.run()
