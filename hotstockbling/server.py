#!/usr/bin/env python

import json

from flask import Flask, request, jsonify

import config
from lager import logger

app = Flask(__name__)


@app.route('/', methods=['POST'])
def message():
    response = '<?xml version="1.0" encoding="UTF-8" ?><Response></Response>'

    form_data = {key: val for key, val in request.form.items()}
    logger.info('Got new Twilio message: {!r}'.format(form_data))

    key = 'raw/{}-{}.json'.format(form_data['From'], form_data['MessageSid'])
    config.S3_CLIENT.put_object(
        Key=key,
        Bucket=config.S3_MESSAGE_BUCKET,
        Body=json.dumps(form_data),
        ContentType='application/json',
    )

    return response, 200, {'content-type': 'application/xml'}


@app.route('/', methods=['GET'])
def fetch():
    resp = config.S3_CLIENT.list_objects(Bucket=config.S3_MESSAGE_BUCKET)
    print(resp)

    files = resp.get('Contents', [])

    return jsonify({'files': [d['Key'] for d in files]})


@app.route('/', methods=['DELETE'])
def delete_all():
    resp = config.S3_CLIENT.list_objects(Bucket=config.S3_MESSAGE_BUCKET)
    print(resp)

    for d in resp.get('Contents', []):
        resp = config.S3_CLIENT.delete_object(
            Key=d['Key'],
            Bucket=config.S3_MESSAGE_BUCKET
        )

    return '', 204


@app.route('/<path:key>', methods=['GET'])
def fetch_file(key):
    resp = config.S3_CLIENT.get_object(
        Key=key,
        Bucket=config.S3_MESSAGE_BUCKET
    )

    print(resp)

    return resp['Body'].read(), 200, {'content-type': resp['ContentType']}


@app.route('/<path:key>', methods=['DELETE'])
def delete_file(key):
    resp = config.S3_CLIENT.delete_object(
        Key=key,
        Bucket=config.S3_MESSAGE_BUCKET
    )

    print(resp)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
