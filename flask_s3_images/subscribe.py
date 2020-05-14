from flask import request, current_app, Blueprint, render_template, redirect

import boto3

blueprint = Blueprint('subscribe', __name__)


@blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'GET':
        return render_template('subscribe.html')
    else:
        email = request.form['email']
        sns_topic_arn = current_app.config['SNS_TOPIC_ARN']
        client = boto3.client('sns', region_name=current_app.config['REGION_NAME'])
        client.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',
            Endpoint=email
        )
        return render_template('success.html')
