import json

# Load the JSON data from accountDataDb.json
with open('accountDataDb.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create dictionaries keyed by string IDs for easy lookup
ACCOUNTS = {str(acc['id']): acc for acc in data['ACCOUNTS']}
CUSTOMERS = {str(cust['id']): cust for cust in data['CUSTOMERS']}
ACCOUNT_TYPES = {str(acc_type['id']): acc_type for acc_type in data['ACCOUNT_TYPES']}

