from requests_oauthlib import OAuth1Session
import requests
import os
import json

my_key = os.environ.get("CONSUMER_KEY")
my_secret = os.environ.get("CONSUMER_SECRET")
my_access_token = os.environ.get("ACCESS_TOKEN")
my_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
##my_key = API_KEY
#my_secret = API_KEY_SECRET
#my_access_token = ACCESS_TOKEN
#my_token_secret = ACCESS_TOKEN_SECRET

def main(event, context):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    responseAPI = requests.get(api_url, headers={'X-Api-Key': '6Q+RVd1Ovqvme9AWyIoaJQ==s7x0uNd4gpBCse9i'})

    if responseAPI.status_code == requests.codes.ok:
        print(responseAPI.text)
    else:
        print("Error:", responseAPI.status_code, responseAPI.text)

    parsed_json = json.loads(responseAPI.text)
    temp = parsed_json[0]["fact"]
    tweet = {}
    tweet["text"] = temp


    oauth = OAuth1Session(
        my_key,
        client_secret = my_secret,
        resource_owner_key = my_access_token,
        resource_owner_secret = my_token_secret
    )

    responseTwitter = oauth.post("https://api.twitter.com/2/tweets",json = tweet)

    if(responseTwitter.status_code != 201):
        raise Exception(
            "Request returned an error: {} {}".format(responseTwitter.status_code,responseTwitter.text)
        )

    print("Response code: {}".format(responseTwitter.status_code))

    json_response = responseTwitter.json()
    print(json.dumps(json_response,indent = 4,sort_keys = True))

