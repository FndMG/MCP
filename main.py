from fastmcp import FastMCP
import logging

from tools.system1.template import TemplateTools
from tools.system2.user import UserTools

from config.config import Config

Config.init() 

mcp = FastMCP(
    name="mcp-api-wrapper",
    instructions="""
Use these APIs to support users.
"""
)

TOOL_CLASSES = [TemplateTools, UserTools]

for tool_class in TOOL_CLASSES:
    instance = tool_class()
    for tool_func in instance.get_tools_list():
        mcp.tool()(tool_func)


def run_server():
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)

def main():
    logging.basicConfig(level=logging.INFO, force=True)
    try:
        run_server()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
