import pytest
import json
import main
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = ".\\main.py"
SERVER_PARAMS = StdioServerParameters(
    command="python", args=[SERVER_PATH]
)

# I have left in the below commented code as an example of what will not work.
# The FastMCP docs state that you should not open clients in your fixture
# https://gofastmcp.com/development/tests#using-fixtures
# I tried it with both autouse = True and False and it would always hang on call_tool
# call in the test function.
# So instead I open and close the client session in each test function.

# @pytest_asyncio.fixture(scope="module", autouse=True)
# async def setup_module():
#     global mcp_session

#     print("Setting up module...")

#     # manage async contexts versus using nested async with statements
#     exit_stack = AsyncExitStack()

#     server_params = StdioServerParameters(
#         command="python", args=[SERVER_PATH]
#     )

#     # start the stdio client using the server parameters
#     stdio_transport = await exit_stack.enter_async_context(
#         stdio_client(server_params)
#     )
#     stdio, write = stdio_transport

#     # get a client session
#     mcp_session = await exit_stack.enter_async_context(
#         ClientSession(stdio, write)
#     )
#     # initialize the session.
#     await mcp_session.initialize()

#     yield

#     print("Tearing down module...")
#     await exit_stack.aclose()


@pytest.mark.asyncio
async def test_get_customer_info_by_id():
    """Connect to an MCP server retrieve the fist customer info"""

    customer_id = 1

    tool_result = await main.get_customer_info_by_id(customer_id)
    tool_result_content = json.loads(tool_result)
    if tool_result_content:
        assert tool_result_content[0]["id"] == customer_id
    else:
        assert False, "No customer info returned"


@pytest.mark.asyncio
async def test_get_customer_info_by_email():
    """Connect to an MCP server retrieve the customer info by email"""

    customer_email = "alice@example.com"

    mcp_session, exit_stack = await get_mcp_session_exit_stack()
    tool_result = await mcp_session.call_tool("get_customer_info_by_email", {"customer_email": customer_email})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content[0]["email"] == customer_email
    else:
        assert False, "No customer info returned"

    await exit_stack.aclose()


@pytest.mark.asyncio
async def test_get_account_info_by_id():
    """Connect to an MCP server retrieve the customer info by email"""

    account_id = 1

    mcp_session, exit_stack = await get_mcp_session_exit_stack()
    tool_result = await mcp_session.call_tool("get_account_info_by_id", {"account_id": account_id})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content[0]["accountId"] == account_id
    else:
        assert False, "No account info returned"

    await exit_stack.aclose()


@pytest.mark.asyncio
async def test_get_accounts_by_customer_id():
    """Connect to an MCP server retrieve the customer info by email"""

    customer_id = 1

    mcp_session, exit_stack = await get_mcp_session_exit_stack()
    tool_result = await mcp_session.call_tool("get_accounts_by_customer_id", {"customer_id": customer_id})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content[0]["customer_Id"] == customer_id
    else:
        assert False, "No account info returned"

    await exit_stack.aclose()


@pytest.mark.asyncio
async def test_get_account_types():
    """Connect to an MCP server retrieve the account types"""

    mcp_session, exit_stack = await get_mcp_session_exit_stack()
    tool_result = await mcp_session.call_tool("get_account_types", {})
    tool_result_content = json.loads(tool_result.content[0].text)
    if tool_result_content:
        assert tool_result_content[0]["id"] == 1
    else:
        assert False, "No account types returned"
    await exit_stack.aclose()


async def get_mcp_session_exit_stack():
    """Helper function to get an MCP client session and exit stack"""

    # manage async contexts versus using nested async with statements
    exit_stack = AsyncExitStack()

    # start the stdio client using the server parameters
    stdio_transport = await exit_stack.enter_async_context(
        stdio_client(SERVER_PARAMS)
    )
    stdio, write = stdio_transport

    # get a client session
    mcp_session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )
    # initialize the session.
    await mcp_session.initialize()

    return mcp_session, exit_stack
