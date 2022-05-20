import functools
import requests
import json
from predict import predict

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# create blueprint
bp = Blueprint('home', __name__, url_prefix='/')

# load twitter API keys
api_key = ''
with open('api_key.json') as json_file:
    api_key = json.load(json_file)


@bp.route('/home', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        # take data from twitter API
        key = request.form['keyword']
        url = f"https://api.twitter.com/2/tweets/search/recent?query={key}"
        payload = {}
        headers = api_key
        response = requests.request("GET", url, headers=headers, data=payload)
        tweets = json.loads(response.text)
        # predict tweet
        for tweet in tweets['data']:
            predict(tweet['text'])
        return tweets

    return render_template('home.html')
