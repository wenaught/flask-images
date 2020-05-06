# Flask Images

It is a simple REST API that allows fetching files from an AWS S3 bucket
and uploading to the bucket.

# Prerequisites

`AWS_PROFILE`, or a combination of `AWS_SECRET_ACCESS_KEY`
and `AWS_ACCESS_KEY_ID` environment variables set, and AWS CLI configured.

# Usage
```
usage: flask-images [-h] [-p PORT] bucket config

Access image storage on S3

positional arguments:
  bucket                S3 bucket name
  config                Configuration file name for MySQL database connection

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to run the app on

To use the script, please provide a JSON configuration file of the following structure:
{
    "host": "server-address",
    "database": "database-name",
    "user": "user",
    "password": "password"
}
```