"""
Test client for sending requests to the MCP server.
Acts as an AI agent substitute.
"""

import asyncio
import httpx
import argparse
import json
from typing import Optional


class MCPTestClient:
    """Test client for MCP server with session management."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp"
        self.session_id: Optional[str] = None
        self.request_id = 0

    def _get_headers(self) -> dict:
        """Get headers with session ID if available."""
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        return headers

    def _next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id

    def _parse_sse_response(self, text: str) -> dict:
        """Parse SSE response and extract JSON data."""
        for line in text.strip().split("\n"):
            if line.startswith("data: "):
                return json.loads(line[6:])
        raise ValueError("No data found in SSE response")

    async def initialize(self) -> dict:
        """Initialize MCP session."""
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers()
            )

            # Save session ID from response header
            if "mcp-session-id" in response.headers:
                self.session_id = response.headers["mcp-session-id"]

            return self._parse_sse_response(response.text)

    async def send_initialized(self) -> None:
        """Send initialized notification."""
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers()
            )

    async def connect(self) -> dict:
        """Initialize and complete handshake."""
        result = await self.initialize()
        await self.send_initialized()
        print(f"Connected with session ID: {self.session_id}")
        return result

    async def call_tool(self, tool_name: str, arguments: Optional[dict] = None) -> dict:
        """Call an MCP tool."""
        if not self.session_id:
            await self.connect()

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers()
            )
            return self._parse_sse_response(response.text)

    async def list_tools(self) -> dict:
        """List available MCP tools."""
        if not self.session_id:
            await self.connect()

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {}
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers()
            )
            return self._parse_sse_response(response.text)


class StubController:
    """Controller for the stub server."""

    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url

    async def set_busy(self, busy: bool, delay: float = 5.0) -> dict:
        """Set stub server busy state."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/stub/config/busy",
                json={"busy": busy, "delay": delay}
            )
            return response.json()

    async def get_busy(self) -> dict:
        """Get stub server busy state."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/stub/config/busy")
            return response.json()

    async def set_delay(self, delay: float) -> dict:
        """Set response delay."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/stub/config/delay",
                params={"delay": delay}
            )
            return response.json()


async def test_normal_flow(mcp_client: MCPTestClient):
    """Test normal API flow."""
    print("\n=== Test: Normal Flow ===")

    print("\n1. List tools:")
    result = await mcp_client.list_tools()
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n2. Get template list:")
    result = await mcp_client.call_tool("get_template_list")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n3. Get template detail (id=1):")
    result = await mcp_client.call_tool("get_template_detail", {"template_id": "1"})
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def test_busy_state(mcp_client: MCPTestClient, stub_ctrl: StubController):
    """Test busy state handling."""
    print("\n=== Test: Busy State ===")

    print("\n1. Set stub to busy:")
    result = await stub_ctrl.set_busy(True, delay=3.0)
    print(json.dumps(result, indent=2))

    print("\n2. Try to get template list (should fail with 503):")
    result = await mcp_client.call_tool("get_template_list")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n3. Reset busy state:")
    result = await stub_ctrl.set_busy(False)
    print(json.dumps(result, indent=2))

    print("\n4. Get template list (should succeed):")
    result = await mcp_client.call_tool("get_template_list")
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def test_delayed_response(mcp_client: MCPTestClient, stub_ctrl: StubController):
    """Test delayed response handling."""
    print("\n=== Test: Delayed Response ===")

    print("\n1. Set 2 second delay:")
    result = await stub_ctrl.set_delay(2.0)
    print(json.dumps(result, indent=2))

    print("\n2. Get template list (should take ~2 seconds):")
    import time
    start = time.time()
    result = await mcp_client.call_tool("get_template_list")
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}s")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n3. Reset delay:")
    await stub_ctrl.set_delay(0.0)


async def main():
    parser = argparse.ArgumentParser(description="MCP Test Client")
    parser.add_argument("--mcp-url", default="http://localhost:8080", help="MCP server URL")
    parser.add_argument("--stub-url", default="http://localhost:8081", help="Stub server URL")
    parser.add_argument("--test", choices=["normal", "busy", "delay", "all"], default="all")
    args = parser.parse_args()

    mcp_client = MCPTestClient(args.mcp_url)
    stub_ctrl = StubController(args.stub_url)

    try:
        if args.test in ["normal", "all"]:
            await test_normal_flow(mcp_client)

        if args.test in ["busy", "all"]:
            await test_busy_state(mcp_client, stub_ctrl)

        if args.test in ["delay", "all"]:
            await test_delayed_response(mcp_client, stub_ctrl)

    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
