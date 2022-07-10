import requests
import json
from flask import current_app
from bs4 import BeautifulSoup


def twitter(keyword):
    # fields to return
    tweet_field = 'created_at,author_id'
    expansions = 'author_id'
    max_result = 10

    url = f"https://api.twitter.com/2/tweets/search/recent?tweet.fields={tweet_field}&expansions={expansions}&max_results={max_result}&query={keyword}"  # noqa: E501
    payload = {}
    headers = {
        "Authorization": "Bearer " + current_app.config['TWITTER_API_KEY']
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    tweets = json.loads(response.text)
    print(tweets)
    return tweets


def getUrl(url):
    req = requests.request("GET", url, headers={'User-Agent': 'Mozilla/5.0'})
    print(req.status_code)
    if req.status_code == 404:
        return req.status_code
    html = req.text
    data = BeautifulSoup(html, 'html.parser')
    return data
