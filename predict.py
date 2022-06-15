import requests
import re
import json
from flask import current_app


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


def predict(text):
    text = preprocess(text)
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

    prediction = {}
    prediction['score'] = output['documentSentiment']['score']
    if prediction['score'] > 0.25:
        prediction['result'] = 'positive'
    elif prediction['score'] < -0.25:
        prediction['result'] = 'negative'
    else:
        prediction['result'] = 'netral'

    return prediction
