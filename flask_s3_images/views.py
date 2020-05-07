from random import choice

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from flask import Response, request, current_app, Blueprint
from werkzeug.utils import secure_filename

import flask_s3_images.database
import flask_s3_images.utilities

view_blueprint = Blueprint('views', __name__)


@view_blueprint.route('/random', methods=['GET'])
def get_random_image():
    try:
        s3 = boto3.client('s3')
        bucket = current_app.config['BUCKET']
        s3_objects = s3.list_objects_v2(Bucket=bucket)
        random_object_key = choice(s3_objects['Contents'])['Key']
        return flask_s3_images.utilities.get_s3_object(s3, bucket, random_object_key)
    except (ClientError, BotoCoreError) as err:
        current_app.logger.error(err)
        return Response(response='Failed to fetch file from S3 with the following error: {}'.format(err), status=500)


@view_blueprint.route('/<image_name>', methods=['GET'])
def get_image(image_name):
    try:
        s3 = boto3.client('s3')
        bucket = current_app.config['BUCKET']
        return flask_s3_images.utilities.get_s3_object(s3, bucket, image_name)
    except (ClientError, BotoCoreError) as err:
        current_app.logger.error(err)
        return Response(response='Failed to fetch file from S3 with the following error: {}'.format(err), status=500)


@view_blueprint.route('/', methods=['POST'])
def upload_image():
    try:
        s3 = boto3.client('s3')
        bucket = current_app.config['BUCKET']
        database = flask_s3_images.database.get_database()
        f = request.files['data']
        file_path = '/tmp/{}'.format(f.filename)
        f.save(file_path)
        database.upload_metadata(file_path)
        s3.upload_file(file_path, bucket, secure_filename(f.filename))
        return Response(response='File uploaded successfully', status=200)
    except KeyError:
        return Response(response='File should be sent with \'data\' key', status=400)
    except (ClientError, BotoCoreError) as err:
        current_app.logger.error(err)
        return Response(response='Failed to upload file to S3 with the following error: {}'.format(err), status=500)


