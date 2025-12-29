import json

# Load the JSON data from accountDataDb.json
with open('accountDataDb.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Copy data into constants for easy access
ACCOUNTS = data['ACCOUNTS']
CUSTOMERS = data['CUSTOMERS']
ACCOUNT_TYPES = data['ACCOUNT_TYPES']
