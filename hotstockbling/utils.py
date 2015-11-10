#!/usr/bin/env python

import json
import urllib

import config
from lager import logger


def log_lambda(event, context):
    logger.info('Running {} v{}'.format(context.function_name, context.function_version))
    logger.info('Event data: {}'.format(json.dumps(event, indent=2)))


def read_s3(bucket, key):
    try:
        response = config.S3_CLIENT.get_object(Bucket=bucket, Key=key)

        raw_body = response['Body'].read()
        logger.info('Processing data: {}'.format(raw_body))

        body = json.loads(raw_body)
    except Exception:
        logger.exception('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise

    return body


def read_s3_from_event(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    return read_s3(bucket, key), bucket, key


def send_sms(message, sender, recipient, bucket):
    key = 'send/{}-{}'.format(recipient, sender)
    config.S3_CLIENT.put_object(Bucket=bucket, Key=key, Body=json.dumps({'message': message}))
