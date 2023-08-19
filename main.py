from flask import Flask, request, jsonify
import hmac
import hashlib
import os
import requests
import json
import jwt
import time
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()



from getResponse import query

app = Flask(__name__)

GITHUB_APP_SECRET=os.getenv('GITHUB_APP_SECRET')
APP_ID = os.getenv('APP_ID')
private_key_path = os.path.join(os.path.dirname(__file__), "jatase.2023-08-19.private-key.pem")

# Secret key for validating webhook payloads
SECRET = os.environ.get(GITHUB_APP_SECRET)
# GitHub API base URL
API_BASE_URL = "https://api.github.com"

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


    if "discussion" in data and "comment" in data:
        discussion = data["discussion"]
        comment = data["comment"]

        # import ipdb; ipdb.set_trace()
        if "body" in comment:  # and "tag" in comment:
            body = comment["body"]
            # tag = comment["tag"]

            if "@jatase" in body:
                # reply_text = f"Thanks for tagging me, @{comment['author']['login']}! 🤖"
                
                body = body.replace("@jatase", "")
                reply_text = f"Thanks for tagging me! 🤖 {query(body)}"
                print(reply_text)
                #import ipdb; ipdb.set_trace()
                reply_to_comment(discussion['repository_url'] + "/discussions", reply_text)

    return "OK", 200

def is_valid_signature(payload, signature):
    calculated_signature = hmac.new(SECRET.encode(), payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest("sha1=" + calculated_signature, signature)

def reply_to_comment(discussion_url, reply_text):
    token = create_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "body": reply_text
    }

    response = requests.post(discussion_url + "/comments", json=data, headers=headers)
    if response.status_code == 201:
        print("Reply posted successfully")
    else:
        print("Failed to post reply:", response.text)


def create_token():
    current_time = int(time.time())
    payload = {
        "iat": current_time,
        "exp": current_time + 600,  # 10 minutes (maximum validity)
        "iss": APP_ID
    }

    with open(private_key_path, "rb") as key_file:
        private_key_data = key_file.read()
        private_key = serialization.load_pem_private_key(private_key_data, password=None)
        token = jwt.encode(payload, private_key, algorithm="RS256")

    return token

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)


