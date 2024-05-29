#SMS 7 Day Sequence

import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests

# Load environment variables from .env file
load_dotenv()

# Define the payload with the required parameters
import requests
import json

# Define your ConvertKit API key and sequence ID
api_key = '<your_public_api_key>'
sequence_id = '<sequence_id>'
email = 'jonsnow@example.com'

# Define the URL for subscribing to a sequence
url = f'https://api.convertkit.com/v3/sequences/{sequence_id}/subscribe'

# Define the payload with the required parameters
payload = {
    "api_key": api_key,
    "email": email
}

# Define the headers with the content type
headers = {
    'Content-Type': 'application/json; charset=utf-8'
}

# Send the POST request to the ConvertKit API
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response from the API
print(response.json())