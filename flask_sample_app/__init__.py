import os

from flask import Flask

from flask_sample_app import (
    db, auth
)

def create_app(test_config=None):
    # create and configure the app
    # instance_relative_config tells the app that the config files are
    # relative to the instance folder(which is located outside the app
    # package) and this can hold different files that shouldn't be commited
    # to verstion control such as secrets, db files, etc.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask_sample_app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World'

    db.init_app(app)

    app.register_blueprint(auth.auth)

    app.add_url_rule("/", endpoint="index")

    return app

