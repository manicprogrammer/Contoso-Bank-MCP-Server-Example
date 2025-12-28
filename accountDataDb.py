import json

# Load the JSON data from accountDataDb.json
with open('accountDataDb.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create dictionaries keyed by string IDs for easy lookup
ACCOUNTS = data['ACCOUNTS']
CUSTOMERS = data['CUSTOMERS']
ACCOUNT_TYPES = data['ACCOUNT_TYPES']
