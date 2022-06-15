import requests
import json
from flask import current_app


def twitter(keyword):
    # take data from twitter API\
    url = f"https://api.twitter.com/2/tweets/search/recent?max_results={current_app.config['TWITTER_API_LIMIT']}&query={keyword}"  # noqa: E501
    payload = {}
    headers = {
        "Authorization": "Bearer " + current_app.config['TWITTER_API_KEY']
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    tweets = json.loads(response.text)
    # print(tweets)
    return tweets
