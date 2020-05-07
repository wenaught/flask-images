import os
import requests

from flask import Flask
import flask_s3_images.database
import flask_s3_images.views


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
    credentials_resp = requests.\
        get('http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance')
    app.config['CREDENTIALS'] = credentials_resp.json()
    app.teardown_appcontext(flask_s3_images.database.close_database)
    app.register_blueprint(flask_s3_images.views.view_blueprint)
    app.logger.info('Instance folder at: {}'.format(app.instance_path))
    return app
