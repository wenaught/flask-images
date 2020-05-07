import os

from flask import Flask
import flask_images.database
import flask_images.views


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_json('config.json', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.teardown_appcontext(flask_images.database.close_database)
    app.register_blueprint()
    return app
