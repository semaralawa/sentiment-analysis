import os
from flask import (Flask, redirect, url_for)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
HTTP_PORT = 80


def create_app():
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import home
    app.register_blueprint(home.bp)

    import auth
    app.register_blueprint(auth.bp)

    # simple route

    @app.route("/")
    def start():
        return redirect(url_for('home.home'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=HTTP_PORT, host='0.0.0.0', use_reloader=True)
