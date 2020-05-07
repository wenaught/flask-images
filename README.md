# Flask S3 Images

It is a simple REST API that allows fetching files from an AWS S3 bucket
and uploading to the bucket.

# Prerequisites

`AWS_PROFILE`, or a combination of `AWS_SECRET_ACCESS_KEY`
and `AWS_ACCESS_KEY_ID` environment variables set, and AWS CLI configured.

# Usage

Please edit `config.json` in Flask instance folder according to your setup before installation:
```json
{
    "DB_CONFIG": {
        "host": "",
        "database": "",
        "user": "",
        "password": ""
    },
    "BUCKET": ""
}
```