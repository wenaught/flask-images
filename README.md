# Flask Images

It is a simple REST API that allows fetching files from an AWS S3 bucket
and uploading to the bucket.

# Prerequisites

`AWS_PROFILE`, or a combination of `AWS_SECRET_ACCESS_KEY`
and `AWS_ACCESS_KEY_ID` environment variables set, and AWS CLI configured.

# Usage

First, please edit `flask_images/config/config.json` according to your setup before installation:
```json
{
    "host": "Database server address",
    "database": "Database name",
    "user": "Database user name",
    "password": "Database user password",
    "bucket": "S3 bucket name"
}
```