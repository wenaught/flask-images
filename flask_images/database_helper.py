import os
from datetime import datetime

import mysql.connector
from PIL import Image
from PIL.ExifTags import TAGS


def transform_datetime(datetime_string):
    return datetime.strptime(datetime_string, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


class DatabaseHelper:
    TABLE = """
    CREATE TABLE IF NOT EXISTS `metadata` (
        `id` int NOT NULL AUTO_INCREMENT,
        `FileName` VARCHAR(255) NOT NULL,
        `DateTime` DATETIME NOT NULL,
        `DateTimeOriginal` DATETIME NOT NULL,
        `DateTimeDigitized` DATETIME NOT NULL,
        `XResolution` DECIMAL (5,2) NOT NULL,
        `YResolution` DECIMAL (5,2) NOT NULL,
        `ResolutionUnit` ENUM('RESUNIT_NONE','RESUNIT_INCH','RESUNIT_CENTIMETER') NOT NULL,
        PRIMARY KEY (`id`)) ENGINE=InnoDB
    """
    INSERT_METADATA = """
    INSERT INTO `metadata`
        (FileName, DateTime, DateTimeOriginal, DateTimeDigitized, XResolution, YResolution, ResolutionUnit)
    VALUES
        (%(FileName)s, %(DateTime)s, %(DateTimeOriginal)s, %(DateTimeDigitized)s,
        %(XResolution)s, %(YResolution)s, %(ResolutionUnit)s)
    """
    METADATA_TRANSFORM = {
        'DateTime': transform_datetime,
        'DateTimeOriginal': transform_datetime,
        'DateTimeDigitized': transform_datetime,
        'XResolution': lambda x: x[0] / x[1],
        'YResolution': lambda x: x[0] / x[1],
        'ResolutionUnit': lambda x: x
    }

    def __init__(self, config_dict, logger):
        self.logger = logger
        self.logger.info('Connecting to database')
        self.connector = mysql.connector.connect(**config_dict)
        self.cursor = self.connector.cursor()
        self.cursor.execute(self.TABLE)
        self.cursor.execute('USE {}'.format(config_dict['database']))

    def upload_metadata(self, image_path):
        image = Image.open(image_path)
        image_metadata = image.getexif()
        image_metadata_dict = {TAGS.get(tag_id, tag_id): image_metadata.get(tag_id) for tag_id in image_metadata}
        upload_metadata_dict = dict()
        for tag in self.METADATA_TRANSFORM.keys():
            upload_metadata_dict[tag] = self.METADATA_TRANSFORM[tag](image_metadata_dict[tag])
        upload_metadata_dict['FileName'] = os.path.split(image_path)[1]
        self.logger.info('Uploading image metadata')
        self.cursor.execute(self.INSERT_METADATA, upload_metadata_dict)
        self.connector.commit()
