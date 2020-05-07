import os
from random import choice
import json

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from flask import send_file, Response, request
from werkzeug.utils import secure_filename

from flask_images.database_helper import DatabaseHelper
from flask_images import app

s3 = boto3.client('s3')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'), 'r') as config_file:
    config_dict = json.loads(config_file.read())

bucket = config_dict.pop('bucket')
helper = DatabaseHelper(config_dict, app.logger)


@app.route('/random', methods=['GET'])
def get_random_image():
    try:
        s3_objects = s3.list_objects_v2(Bucket=bucket)
        random_object_key = choice(s3_objects['Contents'])['Key']
        return get_s3_object(random_object_key)
    except (ClientError, BotoCoreError) as err:
        app.logger.error(err)
        return Response(response='Failed to fetch file from S3 with the following error: {}'.format(err), status=500)


@app.route('/<image_name>', methods=['GET'])
def get_image(image_name):
    try:
        return get_s3_object(image_name)
    except (ClientError, BotoCoreError) as err:
        app.logger.error(err)
        return Response(response='Failed to fetch file from S3 with the following error: {}'.format(err), status=500)


@app.route('/', methods=['POST'])
def upload_image():
    try:
        f = request.files['data']
        file_path = '/tmp/{}'.format(f.filename)
        f.save(file_path)
        helper.upload_metadata(file_path)
        s3.upload_file(file_path, bucket, secure_filename(f.filename))
        return Response(response='File uploaded successfully', status=200)
    except KeyError:
        return Response(response='File should be sent with \'data\' key', status=400)
    except (ClientError, BotoCoreError) as err:
        app.logger.error(err)
        return Response(response='Failed to upload file to S3 with the following error: {}'.format(err), status=500)


def get_s3_object(object_key):
    file_path = '/tmp/{}'.format(object_key)
    s3.download_file(bucket, object_key, file_path)
    return send_file(file_path)
