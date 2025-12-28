import pytest
import pytest_asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json  # Add at top

SERVER_PATH = ".\\main.py"
mcp_session = None

"""@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_module():
    global mcp_session

    print("Setting up module...")
    
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
    mcp_session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )
    # initialize the session.
    await mcp_session.initialize()

    yield 
    
    print("Tearing down module...")
    #await exit_stack.aclose()
"""

@pytest.mark.asyncio
async def test_get_customer_info_by_id():
    """Connect to an MCP server retrieve the fist customer info"""

    customer_id = "1"

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
    mcp_session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )
    # initialize the session.
    await mcp_session.initialize()

    tool_result = await mcp_session.call_tool("get_customer_info_by_id", {"customer_id": customer_id})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content["id"] == int(customer_id)
    else:
        assert False, "No customer info returned"
    await exit_stack.aclose()


@pytest.mark.asyncio
async def test_get_customer_info_by_email():
    """Connect to an MCP server retrieve the customer info by email"""
    
    customer_email = "alice@example.com"

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
    mcp_session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )
    # initialize the session.
    await mcp_session.initialize()

    tool_result = await mcp_session.call_tool("get_customer_info_by_email", {"customer_email": customer_email})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content[0]["email"] == customer_email
    else:
        assert False, "No customer info returned"

    await exit_stack.aclose()