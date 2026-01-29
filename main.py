from fastmcp import FastMCP
from os import getenv
import logging

from tools.template import TemplateTools

mcp = FastMCP(
    name="mcp-api-wrapper",
    instructions="""
Use these APIs to support users.
If required parameters are missing, ask the user for them.
"""
)

TOOL_CLASSES = [TemplateTools]

for tool_class in TOOL_CLASSES:
    instance = tool_class()
    for tool_func in instance.get_tools_list():
        mcp.tool()(tool_func)


def run_server():
    print(f"Hello from mcp-api-wrapper! API_HOST_NAME={getenv('API_HOST_NAME')}")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)

def main():
    logging.basicConfig(level=logging.INFO, force=True)
    try:
        run_server()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
