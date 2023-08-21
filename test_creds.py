import requests
import os
import jwt
import platform
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()

SERGE_COMPUTER = 'Serges-MBP.lan'

if platform.node() == SERGE_COMPUTER:
    private_key_path = os.path.join(os.path.dirname(__file__), "jatase.2023-08-19.private-key.pem") # Replace with your private key file path
else:
    private_key_path = os.path.join(os.path.dirname(__file__), "jatasabot.2023-08-19.private-key.pem") # Replace with your private key file path

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

if platform.node() == SERGE_COMPUTER:
    installation_id = '40882687'
else:
    installation_id = '40888424'

response = requests.post(
    f"https://api.github.com/app/installations/{installation_id}/access_tokens",
    headers=headers
)

print(response.status_code)
if response.status_code == 201:
    installation_token = response.json()["token"]
    print("Installation token:", installation_token)
else:
    print("Failed to get installation token:", response.text)

owner = 'skoudoro'
repo = 'ghbot'
discussion_number = 3
token = installation_token
graphql_endpoint = "https://api.github.com/graphql"
# comment_text = "My first reply ! Thanks for tagging me! 🤖"
# comment_text = "I am a bot Replying 🤖 ! "
comment_text = "Last test with the bot Replying 🤖 ! "


###  Test if we can get the discussion comments
# a way to validate disccusion id
query = """
query GetDiscussionComments($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      id
      comments(first: 100) {
        totalCount
        nodes {
          id
          body
          author {
            login
          }
        }
      }
    }
  }
}
"""

variables = {
    "owner": owner,
    "repo": repo,
    "number": discussion_number
}

headers = {
    'Authorization': f'Bearer {installation_token}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.post(graphql_endpoint, json={"query": query, "variables": variables}, headers=headers)

discussion_id = ''
if response.status_code == 200:
    data = response.json()
    # import ipdb; ipdb.set_trace()
    # comments =data["data"]["repository"]["discussion"]["comments"]
    discussion_id = data["data"]["repository"]["discussion"]["id"]
    print("we got some discussion comments")

else:
    print(f"Request failed with status code: {response.status_code}")


# url = f'https://api.github.com/repos/{owner}/{repo}/discussions'

mutation = """
    mutation AddDiscussionComment($input: AddDiscussionCommentInput!) {
      addDiscussionComment(input: $input) {
        comment {
          id
          body
        }
      }
    }
    """

variables = {
        "input": {
            "discussionId": discussion_id,
            "body": comment_text
        }
    }

headers = {
    'Authorization': f'Bearer {installation_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# response = requests.get(url, headers=headers)
response = requests.post(graphql_endpoint, json={"query": mutation, "variables": variables}, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")