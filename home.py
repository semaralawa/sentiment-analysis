# import functools
from predict import predict
import getData

from flask import (
    Blueprint, render_template, request
)

# create blueprint
bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('dashboard.html')


@bp.route('/result', methods=('GET', 'POST'))
def result():
    if request.method == 'POST':
        print(request.form)
        key = request.form['keyword']
        if (request.form.get('twitter')):
            print('anjay')

        # get data from every sources
        tweets = getData.twitter(key)

        # predict tweet
        predict_result = []
        for tweet in tweets['data']:
            # print(tweet)
            result = predict(tweet['text'])
            tweet.update(result)
            print(tweet)
            predict_result.append(tweet)

        # print(predict_result)

        return render_template('tables.html', datas=predict_result)


@bp.route('/test', methods=('GET', 'POST'))
def test():
    return render_template('tables.html')
