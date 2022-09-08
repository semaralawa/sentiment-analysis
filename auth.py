import json
import JWT
from flask import (
    Blueprint, redirect, url_for, session, current_app, request
)
import requests
import uuid

# create blueprint
bp = Blueprint('auth', __name__, url_prefix='/')


def authenticateToSSO():
    payload = {
        'redirect': request.host_url + 'authData',
        'urlToRedirect': request.url,
        'logoutLink': request.host_url + 'logout',
        'kode_broker': current_app.config['BROKER_CODE'],
        'sessionRequest': session['id']
    }
    JWT_token = JWT.encodeJWT(payload)
    return JWT_token.decode('ascii')


@bp.before_app_request
def load_logged_in_user():
    # exclude /authData route
    if ('/authData/' in request.path):
        return
    if ('/guest' in request.path):
        return

    if session.get('id') is None or session.get('is_verify') is None:
        session.clear()
        session['id'] = uuid.uuid1().hex
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
        session['is_verify'] = 1
        decoded = JWT.decodeJWT(data_in['data'].encode('ascii'))
        print(decoded)
        session['is_login'] = 1
        # save some data from SSO
        session['user_id'] = decoded['user']['id']
        session['user_fullname'] = decoded['user']['name']
        session['username'] = decoded['user']['username']
        session['user_email'] = decoded['user']['email']
        session['user_profilepic'] = decoded['user']['profilepic']

        return redirect(decoded['urlToRedirect'])
    else:
        print('login gagal')


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    logout_link = current_app.config['SSO_DOMAIN'] + 'logout'
    return redirect(logout_link)
