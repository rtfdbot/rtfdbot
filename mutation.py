 
    
    
# steps 

# private key path
# app_id
# installation_id
# repository_owner
# repository_name


# load private key
# generate jwt
# request installation id
# request installation token
# Authenticate  * 
# - inlcude jwt in authori
# Use the installation token for API requests
# GraphQL queries

mutation = """
{
  addDiscussionComment(input: {
    discussionId: "3",
    body: "Your reply here",
    clientMutationId: "13456"
  }) {
   # response type:
   comment{
    id
    }
  }
}

"""


api_url = f'https://api.github.com/graphql'
api_headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.post(api_url, json={'query': mutation}, headers=api_headers)

if response.status_code == 200:
    data = response.json()
    comments = data['data']['repository']['discussion']['comments']['nodes']
    comment_data = data['data']['addComment']['commentEdge']['node']
    print(comment_data, comments)
else:
    print(f"Request failed with status code: {response.status_code}")
