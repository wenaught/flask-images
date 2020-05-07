from datetime import datetime

from flask import send_file


def transform_datetime(datetime_string):
    return datetime.strptime(datetime_string, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


METADATA_TRANSFORM = {
    'DateTime': transform_datetime,
    'DateTimeOriginal': transform_datetime,
    'DateTimeDigitized': transform_datetime,
    'XResolution': lambda x: x[0] / x[1],
    'YResolution': lambda x: x[0] / x[1],
    'ResolutionUnit': lambda x: x
}


def get_s3_object(s3_client, bucket, object_key):
    file_path = '/tmp/{}'.format(object_key)
    s3_client.download_file(bucket, object_key, file_path)
    return send_file(file_path)
