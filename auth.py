import json
import JWT
from flask import (
    Blueprint, redirect, url_for, session, current_app
)
import requests
import uuid

# create blueprint
bp = Blueprint('auth', __name__, url_prefix='/')


def authenticateToSSO():
    payload = {
        'redirect': 'http://localhost/authData',
        'urlToRedirect': 'http://localhost/home',
        'logoutLink': current_app.config['SSO_DOMAIN'] + 'logout',
        'kode_broker': current_app.config['BROKER_CODE'],
        'sessionRequest': session['id']
    }
    JWT_token = JWT.encodeJWT(payload)
    return JWT_token.decode('ascii')


@bp.before_app_request
def load_logged_in_user():
    # for testing
    # session.clear()

    is_login = session.get('id')
    if is_login is None:
        session.clear()
        session['id'] = uuid.uuid1().hex
        print(session.get('id'))
        token = authenticateToSSO()
        return redirect(current_app.config['SSO_DOMAIN'] + 'authBroker/' + token)  # noqa: E501


@bp.route('/authData/<token>', methods=('GET', 'POST'))
def authData(token):
    # verify on SSO
    url = current_app.config['SSO_DOMAIN'] + "api/v1/auth/jwt/verify"
    payload = {'token': token}
    files = []
    headers = {}
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    data_in = json.loads(response.text)

    # get decoded data
    if data_in['status']:
        decoded = JWT.decodeJWT(data_in['data'].encode('ascii'))
        print(decoded)
        session['is_login'] = 1
        return redirect(url_for('home.home'))
    else:
        print('login gagal')
