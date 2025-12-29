import pandas as pd
from mcp.server.fastmcp import FastMCP
from accountDataDb import ACCOUNTS, CUSTOMERS, ACCOUNT_TYPES

mcp = FastMCP("banking-account-info", instructions="Retrieve banking account information for customers")


@mcp.tool()
async def get_customer_info_by_id(customer_id: int):
    """Search for customer info and email address using their unique identifier"""

    df = pd.DataFrame(CUSTOMERS)
    filtered_df = df[df['id'] == customer_id]
    customer_info = filtered_df.to_json(orient='records', indent=None)

    if not customer_info:
        return "No customer by that identifier was found."

    return customer_info


@mcp.tool()
async def get_customer_info_by_email(customer_email: str):
    """Search for customer info by email address"""

    df = pd.DataFrame(CUSTOMERS)
    filtered_df = df[df['email'] == customer_email]
    customer_info = filtered_df.to_json(orient='records', indent=None)

    if not customer_info:
        return "No customer with that email was found."

    return customer_info


@mcp.tool()
async def get_account_info_by_id(account_id: int):
    """Search for account info using the account's unique identifier"""

    accounts_df = pd.DataFrame(ACCOUNTS)
    accounts_filtered_df = accounts_df[accounts_df['id'] == account_id]
    # doing some magic so we don't end up with column name conflicts during the merges
    accounts_filtered_df = accounts_filtered_df.rename(columns={"id": "accountId"})
    customers_df = pd.DataFrame(CUSTOMERS)
    # doing some magic so we don't end up with column name conflicts during the merges
    customers_df = customers_df.rename(columns={"id": "customer_Id"})
    merged_df = pd.merge(accounts_filtered_df, customers_df, left_on="customerId", right_on="customer_Id")
    account_types_df = pd.DataFrame(ACCOUNT_TYPES)
    # doing some magic so we don't end up with column name conflicts during the merges
    account_types_df = account_types_df.rename(columns={"id": "accountType_Id"})
    merged_df = pd.merge(merged_df, account_types_df, left_on="accountType", right_on="accountType_Id")
    account_info = merged_df.to_json(orient='records', indent=None)

    if not account_info:
        return "No account by that identifier was found."

    return account_info


@mcp.tool()
async def get_accounts_by_customer_id(customer_id: int):
    """Retrieve all accounts associated with a given customer identifier"""

    accounts_df = pd.DataFrame(ACCOUNTS)
    accounts_filtered_df = accounts_df[accounts_df['customerId'] == customer_id]
    # doing some magic so we don't end up with column name conflicts during the merges
    accounts_filtered_df = accounts_filtered_df.rename(columns={"id": "accountId"})
    customers_df = pd.DataFrame(CUSTOMERS)
    # doing some magic so we don't end up with column name conflicts during the merges
    customers_df = customers_df.rename(columns={"id": "customer_Id"})
    merged_df = pd.merge(accounts_filtered_df, customers_df, left_on="customerId", right_on="customer_Id")
    account_types_df = pd.DataFrame(ACCOUNT_TYPES)
    # doing some magic so we don't end up with column name conflicts during the merges
    account_types_df = account_types_df.rename(columns={"id": "accountType_Id"})
    merged_df = pd.merge(merged_df, account_types_df, left_on="accountType", right_on="accountType_Id")
    accounts_info = merged_df.to_json(orient='records', indent=None)
    
    if not accounts_info:
        return "No accounts found for that customer Id."

    return accounts_info


@mcp.tool()
async def get_account_types():
    """Retrieve a list of account types"""

    df = pd.DataFrame(ACCOUNT_TYPES)
    account_types = df.to_json(orient='records', indent=None)

    if not account_types:
        return "No account types were found."

    return account_types


if __name__ == "__main__":
    mcp.run()
