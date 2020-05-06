import argparse
from random import choice

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from flask import Flask, send_file, Response, request
from werkzeug.utils import secure_filename

from flask_images.database_helper import DatabaseHelper

s3 = boto3.client('s3')
app = Flask('flask_images')
DEFAULT_PORT = 8080

parser_epilog = """To use the script, please provide a JSON configuration file of the following structure:
{
    "host": "server-address",
    "database": "database-name",
    "user": "user",
    "password": "password"
}
"""
parser = argparse.ArgumentParser(prog='flask-images',
                                 description='Access image storage on S3',
                                 epilog=parser_epilog,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('bucket', type=str, help='S3 bucket name')
parser.add_argument('config', type=str, help="Configuration file name for database connection")
parser.add_argument('-p', '--port', type=int, help='Port to run the app on', default=8080)
args = parser.parse_args()

helper = DatabaseHelper(args.config, app.logger)


@app.route('/random', methods=['GET'])
def get_random_image():
    try:
        s3_objects = s3.list_objects_v2(Bucket=args.bucket)
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
        s3.upload_file(file_path, args.bucket, secure_filename(f.filename))
        return Response(response='File uploaded successfully', status=200)
    except KeyError:
        return Response(response='File should be sent with \'data\' key', status=400)
    except (ClientError, BotoCoreError) as err:
        app.logger.error(err)
        return Response(response='Failed to upload file to S3 with the following error: {}'.format(err), status=500)


def get_s3_object(object_key):
    file_path = '/tmp/{}'.format(object_key)
    s3.download_file(args.bucket, object_key, file_path)
    return send_file(file_path)


def main():
    app.run(port=args.port)


if __name__ == '__main__':
    main()
