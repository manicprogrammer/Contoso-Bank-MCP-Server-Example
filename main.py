import asyncio
from mcp.server.fastmcp import FastMCP
from accountDataDb import ACCOUNTS, CUSTOMERS, ACCOUNT_TYPES

mcp = FastMCP("banking-account-info", instructions="Retrieve banking account information for customers")


@mcp.tool()
async def get_customer_info_by_id(customer_id: str) -> str:
    """Search for customer info and email address using their unique identifier"""

    customer_info = CUSTOMERS.get(customer_id)

    if not customer_info:
        return "No customer by that identifier was found."

    return str(customer_info)


@mcp.tool()
async def get_customer_info_by_email(customer_email: str) -> str:
    """Search for customer info by email address"""

    customer_info = CUSTOMERS.get(customer_email)

    if not customer_info:
        return "No customer with that email was found."

    return str(customer_info)


if __name__ == "__main__":
    mcp.run()
