import os

import mysql.connector
from flask import current_app
from PIL import Image
from PIL.ExifTags import TAGS

import flask_s3_images.utilities


class Database:
    def __init__(self, config_dict, logger):
        self.logger = logger
        self.logger.info('Connecting to database')
        self.connector = mysql.connector.connect(**config_dict)
        self.cursor = self.connector.cursor()
        with current_app.open_resource('resources/schema.sql') as f:
            self.cursor.execute(f.read().decode('utf8'))
        self.cursor.execute('USE {}'.format(config_dict['database']))

    def upload_metadata(self, image_path):
        image = Image.open(image_path)
        image_metadata = image.getexif()
        image_metadata_dict = {TAGS.get(tag_id, tag_id): image_metadata.get(tag_id) for tag_id in image_metadata}
        upload_metadata_dict = dict()
        for tag in flask_s3_images.utilities.METADATA_TRANSFORM.keys():
            upload_metadata_dict[tag] = flask_s3_images.utilities.METADATA_TRANSFORM[tag](image_metadata_dict[tag])
        upload_metadata_dict['FileName'] = os.path.split(image_path)[1]
        self.logger.info('Uploading image metadata')
        with current_app.open_resource('resources/insert_metadata.sql') as f:
            self.cursor.execute(f.read().decode('utf8'), upload_metadata_dict)
        self.connector.commit()

    def close_connection(self):
        self.cursor.close()
        self.connector.close()


def get_database():
    if not hasattr(current_app, 'database'):
        current_app.database = Database(current_app.config['DB_CONFIG'], current_app.logger)
    return current_app.database


def close_database(e=None):
    db = getattr(current_app, 'database', None)
    if db is not None:
        db.close_connection()
        delattr(current_app, 'database')
