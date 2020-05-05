import boto3
from os import environ
from random import choice
from botocore.exceptions import ClientError, BotoCoreError
from flask import Flask, send_file, Response, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET_NAME = environ.get('BUCKET_NAME')


@app.route('/random', methods=['GET'])
def get_random_image():
    try:
        s3_objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
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
        s3.upload_fileobj(f, BUCKET_NAME, secure_filename(f.filename))
    except KeyError:
        return Response(response='File should be sent with \'data\' key', status=400)
    except (ClientError, BotoCoreError) as err:
        app.logger.error(err)
        return Response(response='Failed to upload file to S3 with the following error: {}'.format(err), status=500)


def get_s3_object(object_key):
    file_path = '/tmp/{}'.format(object_key)
    s3.download_file(BUCKET_NAME, object_key, file_path)
    return send_file(file_path)


app.run(port=8080)
