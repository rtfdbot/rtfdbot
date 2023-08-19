import requests
import os
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()

private_key_path = os.path.join(os.path.dirname(__file__), "jatase.2023-08-19.private-key.pem") # Replace with your private key file path

app_id = os.getenv('APP_ID')
now = datetime.utcnow()

with open(private_key_path, 'rb') as key_file:
    private_key_data = key_file.read()

private_key = serialization.load_pem_private_key(private_key_data, password=None)


payload = {
    'iat': now,
    'exp': now + timedelta(minutes=10),
    'iss': app_id
}

jwt_token = jwt.encode(payload, private_key, algorithm='RS256')


headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github.v3+json"
}

installation_id = '40882687'
response = requests.post(
    f"https://api.github.com/app/installations/{installation_id}/access_tokens",
    headers=headers
)

if response.status_code == 201:
    installation_token = response.json()["token"]
    print("Installation token:", installation_token)
else:
    print("Failed to get installation token:", response.text)

import ipdb; ipdb.set_trace()
owner = 'skoudoro'
repo = 'ghbot'
discussion_number = '3'
token = installation_token
graphql_endpoint = "https://api.github.com/graphql"

# url = f'https://api.github.com/repos/{owner}/{repo}/discussions'

query = """
query {
  repository(owner: "%s", name: "%s") {
    discussions(first: 100) {
      edges {
        node {
          title
          url
        }
      }
    }
  }
}
""" % (owner, repo)


headers = {
'Authorization': f'Bearer {installation_token}',
'Accept': 'application/vnd.github.v3+json'
}

# response = requests.get(url, headers=headers)
response = requests.post(graphql_endpoint, json={"query": query}, headers=headers)
import ipdb; ipdb.set_trace()
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")