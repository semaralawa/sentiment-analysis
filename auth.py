import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(username == 'admin' and password == 'aaa'):
            return redirect(url_for('home.home'))
        else:
            flash('username / password salah')

    return render_template('login.html')
