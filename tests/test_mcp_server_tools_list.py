import pytest
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = ".\\main.py"
EXPECTED_TOOLS = [
    "get_customer_info_by_id",
    "get_customer_info_by_email",
    "get_account_info_by_id",
    "get_accounts_by_customer_id",
]


@pytest.mark.asyncio
async def test_mcp_server_tools_list():
    """Connect to an MCP server and verify the list of tools"""

    # manage async contexts versus using nested async with statements
    exit_stack = AsyncExitStack()

    server_params = StdioServerParameters(
        command="python", args=[SERVER_PATH]
    )

    # start the stdio client using the server parameters
    stdio_transport = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    stdio, write = stdio_transport

    # get a client session
    session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )

    # initialize the session.
    # don't need the async conext manager as calling an async method in an existing object
    await session.initialize()

    tools_result = await session.list_tools()
    tools = tools_result.tools
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [tool.description for tool in tools]

    print("\nMCP Server Tools:")
    for tool_name, tool_description in zip(tool_names, tool_descriptions):
        print(f"{tool_name}: {tool_description}")

    assert sorted(EXPECTED_TOOLS) == sorted(tool_names)

    await exit_stack.aclose()
