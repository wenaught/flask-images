import os

from flask import Flask
import flask_s3_images.database
import flask_s3_images.api
import flask_s3_images.subscribe


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
    app.teardown_appcontext(flask_s3_images.database.close_database)
    app.register_blueprint(flask_s3_images.api.blueprint)
    if "SNS_TOPIC_ARN" in app.config:
        app.register_blueprint(flask_s3_images.subscribe.blueprint)
    app.logger.info('Instance folder at: {}'.format(app.instance_path))
    return app
