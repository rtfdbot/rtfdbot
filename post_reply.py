import requests
import os
from dotenv import load_dotenv

graphql_endpoint = "https://api.github.com/graphql"
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')

print(github_token)

headers = {
    'Authorization': f'Bearer {github_token}',
    'Content-Type': 'application/json'
}

mutation = """
mutation CreateComment($discussionId: ID!, $body: String!) {
  addComment(input: {discussionId: $discussionId, body: $body}) {
    comment {
      id
      body
    }
  }
}
"""

query = """
{
  viewer {
    login
    repository(name: "ghbot") {
      discussion(number: 1) {
        id
        author {
          login
        }
        body
      }
    }
  }
}
"""

variables = {
    "discussionId": "DISCUSSION_ID_HERE",
    "body": "Your comment here"
}

response = requests.post(graphql_endpoint, json={"query": query, "variables": variables}, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")


'''

# create a reply to a discussion

print("create a reply to a discussion")

mutation = """
mutation AddReplyToDiscussion($body: String!, $discussionId: ID!) {
  addDiscussionComment(input: {body: $body, discussionId: $discussionId}) {
    comment {
      id
      body
    }
  }
}
"""

variables = {
    "body": "Response from ghbot:\n\n ghbot is awesome!",
    "discussionId": "D_kwDOKJZ8gM4AVI2h"
}

response = requests.post(graphql_endpoint, json={"query": mutation, "variables": variables}, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")

'''