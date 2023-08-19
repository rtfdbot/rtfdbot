from flask import Flask, request, jsonify
import hmac
import hashlib
import os
import requests
import json

app = Flask(__name__)

GITHUB_APP_SECRET="ca0d4f4ba98f15b7e234df0d55882ca7390e321e"
GITHUB_APP_TOKEN=""

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
        if "body" in comment and "tag" in comment:
            body = comment["body"]
            tag = comment["tag"]

            if "@jatase" in body:
                reply_text = f"Thanks for tagging me, @{comment['author']['login']}! 🤖"
                reply_to_comment(discussion["url"], reply_text)

    return "OK", 200

def is_valid_signature(payload, signature):
    calculated_signature = hmac.new(SECRET.encode(), payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest("sha1=" + calculated_signature, signature)

def reply_to_comment(discussion_url, reply_text):
    headers = {
        "Authorization": f"Bearer {os.environ.get(GITHUB_APP_TOKEN)}"
    }
    data = {
        "body": reply_text
    }
    response = requests.post(discussion_url + "/comments", json=data, headers=headers)
    if response.status_code == 201:
        print("Reply posted successfully")
    else:
        print("Failed to post reply:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)


