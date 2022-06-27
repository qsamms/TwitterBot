from requests_oauthlib import OAuth1Session
import requests
import os
import json
import schedule

my_key = os.environ.get("CONSUMER_KEY")
my_secret = os.environ.get("CONSUMER_SECRET")
my_access_token = os.environ.get("ACCESS_TOKEN")
my_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

responseAPI = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
data = responseAPI.text
parse_json = json.loads(data)
temp = parse_json['text']

tweet = {}
tweet['text'] = temp

oauth = OAuth1Session(
    my_key,
    client_secret = my_secret,
    resource_owner_key = my_access_token,
    resource_owner_secret = my_token_secret
)

response = oauth.post("https://api.twitter.com/2/tweets",json = tweet)

if(response.status_code != 201):
    raise Exception(
        "Request returned an error: {} {}".fomrat(response.stauts_code,response.text)
    )

print("Response code: {}".format(response.status_code))

json_response = response.json()
print(json.dumps(json_response,indent = 4,sort_keys = True))