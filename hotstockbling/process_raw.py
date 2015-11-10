#!/usr/bin/env python

import json

import config
import utils
from lager import logger


def lambda_handler(event, context):
    utils.log_lambda(event, context)

    body, bucket, key = utils.read_s3_from_event(event)

    message = body['Body']
    requested_command = None
    for command in ('helpme', 'details', 'buy', 'sell'):
        if message.lower().startswith(command):
            requested_command = command
            break

    requested_command = requested_command or 'overview'
    new_key = key.replace('raw', requested_command, 1)

    try:
        config.S3_CLIENT.put_object(
            Key=new_key,
            Bucket=bucket,
            Body=json.dumps(body),
            ContentType='application/json',
        )
    except Exception:
        logger.exception('Could not upload data to {}'.format(new_key))
        raise

    # FIXME: If this is the first time the user has contacted us, send them the help message
    if False:
        help_key = key.replace('raw', 'help', 1)
        try:
            config.S3_CLIENT.put_object(
                Key=help_key,
                Bucket=bucket,
                Body=json.dumps(body),
                ContentType='application/json',
            )
        except Exception:
            logger.exception('Could not start help message workflow {}'.format(help_key))
