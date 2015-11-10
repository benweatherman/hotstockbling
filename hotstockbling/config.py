#!/usr/bin/env python

import os

import boto3

from lager import logger

try:
    import local_config
    logger.info('Imported local config {}'.format(local_config))
except:
    pass

S3_MESSAGE_BUCKET = 'hotstockbling.messages'

SESSION = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-west-2')
S3_CLIENT = SESSION.client('s3')
