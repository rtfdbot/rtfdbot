from flask import Flask, request, jsonify
import hmac
import hashlib
import os
import requests
import json
import jwt
import time
import platform
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()



from getResponse import query

app = Flask(__name__)

SERGE_COMPUTER = 'Serges-MBP.lan'
GITHUB_APP_SECRET=os.getenv('GITHUB_APP_SECRET')
APP_ID = os.getenv('APP_ID')
private_key_path = os.path.join(os.path.dirname(__file__), "jatase.2023-08-19.private-key.pem")

# Secret key for validating webhook payloads
SECRET = os.environ.get(GITHUB_APP_SECRET)
# GitHub API base URL
GH_API_BASE_URL = "https://api.github.com"
GH_GRAPHQL_URL = "https://api.github.com/graphql"


@app.route("/", methods=["GET"])
def homepage():
    return 'hello my world'


@app.route("/callback", methods=["GET"])
def callback():
    print("callback")
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    print("we succeeded webhook")

    # Todo: add a webhook secret
    # signature = request.headers.get("X-Hub-Signature")
    # if not signature or not is_valid_signature(request.data, signature):
    #     return "Invalid signature", 403
    data = request.json
    installation_id = data["installation"]["id"]

    if "discussion" in data and "comment" in data:
        discussion = data["discussion"]
        comment = data["comment"]

        if "body" in comment:  # and "tag" in comment:
            body = comment["body"]
            # tag = comment["tag"]

            if "@jatase" in body:
                # reply_text = f"Thanks for tagging me, @{comment['author']['login']}! 🤖"

                body = body.replace("@jatase", "")
                # Todo:  Setup llama-index and openai API keys
                # reply_text = f"Thanks for tagging me! 🤖 {query(body)}"
                reply_text = f"Thanks for tagging me! 🤖  I am missing some API keys for openai and llama-index. Contact developers and I will be able to answer you."
                print(reply_text)

                reply_to_comment(discussion, reply_text, installation_id)

    return "OK", 200


def is_valid_signature(payload, signature):
    calculated_signature = hmac.new(SECRET.encode(), payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest("sha1=" + calculated_signature, signature)


def reply_to_comment(discussion, reply_text, installation_id):
    discussion_id = discussion["node_id"]
    token = create_token(installation_id)

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
                "body": reply_text
            }
        }

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # response = requests.get(url, headers=headers)
    response = requests.post(GH_GRAPHQL_URL, json={"query": mutation,
                                                   "variables": variables},
                             headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")


def create_token(installation_id):
    current_time = int(time.time())
    payload = {
        "iat": current_time,
        "exp": current_time + 600,  # 10 minutes (maximum validity)
        "iss": APP_ID
    }

    if platform.node() == SERGE_COMPUTER:
        private_key_path = os.path.join(os.path.dirname(__file__), "jatase.2023-08-19.private-key.pem") # Replace with your private key file path
    else:
        private_key_path = os.path.join(os.path.dirname(__file__), "jatasabot.2023-08-19.private-key.pem") # Replace with your private key file path

    with open(private_key_path, "rb") as key_file:
        private_key_data = key_file.read()

    private_key = serialization.load_pem_private_key(private_key_data,
                                                     password=None)
    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers
    )

    installation_token = ''
    if response.status_code == 201:
        installation_token = response.json()["token"]
        print("Installation token:", installation_token)
    else:
        print("Failed to get installation token:", response.text)

    return installation_token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)


