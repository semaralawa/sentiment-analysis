import requests
import re
import json
from datetime import date, datetime
from flask import (
    Blueprint, request, url_for, redirect, current_app
)
import getData
from app import db

# create blueprint
bp = Blueprint('predict', __name__, url_prefix='/')


def preprocess(text):
    # Defining regex patterns.
    url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    user_pattern = '@[^\s]+'
    alpha_pattern = "[^a-zA-Z0-9]"
    sequence_pattern = r"(.)\1\1+"
    seq_replace_pattern = r"\1\1"

    # preprocess text
    # Replace all URls with 'URL'
    text = re.sub(url_pattern, ' URL', text)
    # Replace @USERNAME to 'USER'.
    text = re.sub(user_pattern, ' USER', text)
    # Replace all non alphabets.
    text = re.sub(alpha_pattern, " ", text)
    # Replace 3 or more consecutive letters by 2 letter.
    text = re.sub(sequence_pattern, seq_replace_pattern, text)

    return text


def predict(source, hist_id, data):
    # text = preprocess(text)
    data['hist_id'] = hist_id

    data['source'] = source
    if 'full text' in data.keys():
        text = text = data['full text'].lower().replace('\n', ' ')
    else:
        text = data['text'].lower().replace('\n', ' ')
    url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=" + current_app.config['GOOGLE_API_KEY']  # noqa: E501
    payload = {
        "encodingType": "UTF8",
        "document": {
            "type": "PLAIN_TEXT",
            "content": text,
            "language": "id"
        }
    }
    headers = {'Content-Type': 'text/plain'}
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    output = json.loads(response.text)
    # print(output)
    data['score'] = output['documentSentiment']['score']
    if data['score'] > 0.25:
        data['result'] = 'positive'
    elif data['score'] < -0.25:
        data['result'] = 'negative'
    else:
        data['result'] = 'neutral'

    db['result'].insert_one(data)
    return data['result']


@bp.route('/predict', methods=('GET', 'POST'))
def predictData():
    if request.method == 'POST':
        print(request.form)
        key = request.form['keyword']

        # make variable and add data
        predict_result = {}
        predict_result['keyword'] = key
        predict_result['date'] = date.today().strftime('%d/%m/%Y')
        predict_result['datetime'] = datetime.now().strftime(
            '%d/%m/%Y %H:%M:%S')
        predict_result['positive'] = 0
        predict_result['negative'] = 0
        predict_result['neutral'] = 0

        hist_id = db['history'].insert_one(predict_result).inserted_id

        if (request.form.get('twitter')):
            # get data from every sources
            tweets = getData.twitter(key)

            # predict tweet
            for tweet in tweets['data']:
                # print(tweet)
                # tweet['date'] = datetime.strftime(datetime.strptime(
                # tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                result = predict('twitter', hist_id, tweet)
                predict_result[result] += 1

        if (request.form.get('news')):
            # get data from news portal
            keyword = key.replace(' ', '+')
            URL = f"https://bmc.baliprov.go.id/search-news?key={keyword}"
            # print(URL)
            data = getData.getUrl(URL)
            table = data.findAll('div', {'class': 'what-cap'})
            for a in table:
                links = a.findAll('a', href=True)
                for link in links:
                    print(link['href'])
                    page = getData.getUrl(link['href'])
                    if page == 404:
                        continue
                    temp = page.findAll('div', {'class': 'section-tittle'})[0]
                    judul = temp.findAll('h3')[0]
                    # print(judul.text.strip())

                    isi = page.findAll('div', {'id': 'news_isi'})[0]
                    teks = isi.findAll('p')
                    allTeks = ''
                    for t in teks:
                        allTeks += t.text.strip()

                    to_predict = {}
                    to_predict['link'] = link['href']
                    to_predict['source'] = 'Bali Media Center'
                    to_predict['text'] = judul.text.strip()
                    to_predict['full text'] = allTeks
                    result = predict('Bali Media Center', hist_id, to_predict)
                    predict_result[result] += 1
                    # print(allTeks)

            # print(predict_result['all_data'])

        # store data to database
        db.history.update_one({"_id": hist_id}, {"$set": predict_result})
        # hist_id = db['history'].insert_one(predict_result).inserted_id
        print(hist_id)
        return redirect(url_for('home.result', data_id=hist_id))
