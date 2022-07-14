from flask import (
    Blueprint, redirect, render_template, url_for, session)
from app import db
import json
from bson import json_util
from bson.objectid import ObjectId

# create blueprint
bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    hist_cursor = db.history.find({'username': session['username']})
    hist_data = []
    for data in hist_cursor:
        hist_data.append(data)
    return render_template('dashboard.html', hist_data=hist_data)


@bp.route('/result/<data_id>', methods=('GET', 'POST'))
def result(data_id):
    hist_data = db.history.find_one({'_id': ObjectId(data_id)})
    result_cursor = db.result.find({'hist_id': ObjectId(data_id)})
    result_data = []
    for data in result_cursor:
        result_data.append(data)
    return render_template('result.html', hist_data=json.loads(json_util.dumps(hist_data)),  # noqa:E501
                           result_data=result_data)


@bp.route('/test', methods=('GET', 'POST'))
def test():
    return render_template('test.html')


@bp.route('/delete/history/<data_id>', methods=('GET', 'POST'))
def deleteHistory(data_id):
    try:
        db['history'].delete_one({'_id': ObjectId(data_id)})
        result = db['result'].delete_many({'hist_id': ObjectId(data_id)})

        print(
            f'successfully delete history with id {data_id} and {result.deleted_count} result')  # noqa: E501
    except Exception as err:
        print(err)

    return redirect(url_for('home.dashboard'))
