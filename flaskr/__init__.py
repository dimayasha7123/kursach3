import os
from flask import Flask
from flaskr.model.model import init_model


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev7123',
        DSN='user=postgres password=postgres7123 dbname=active_citizen sslmode=disable',
        COUNT_OF_PROBS = 3,
        JSON_SORT_KEYS = False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    with app.app_context():
        init_model(db.get_db())

    from . import appeal
    app.register_blueprint(appeal.bp)

    @app.route('/hello')
    def hello():
        return 'Hello from Flask'

    return app
