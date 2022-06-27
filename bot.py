from requests_oauthlib import OAuth1Session
import requests
import os
import json

my_key = os.environ.get("CONSUMER_KEY")
my_secret = os.environ.get("CONSUMER_SECRET")

responseAPI = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
data = responseAPI.text
parse_json = json.loads(data)
temp = parse_json['text']

tweet = {}
tweet['text'] = temp

request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(my_key,client_secret = my_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("Error with consumer key or secret")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print(f"OAuth token: {resource_owner_key}")

base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print(f"Please go here and authorize: {authorization_url}")
verifier = input("Paste the PIN here: ")

access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    my_key,
    client_secret = my_secret,
    resource_owner_key = resource_owner_key,
    resource_owner_secret = resource_owner_secret,
    verifier = verifier
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

oauth = OAuth1Session(
    my_key,
    client_secret = my_secret,
    resource_owner_key = access_token,
    resource_owner_secret = access_token_secret
)

response = oauth.post("https://api.twitter.com/2/tweets",json = tweet)

if(response.status_code != 201):
    raise Exception(
        "Request returned an error: {} {}".fomrat(response.stauts_code,response.text)
    )

print("Response code: {}".format(response.status_code))

json_response = response.json()
print(json.dumps(json_response,indent = 4,sort_keys = True))