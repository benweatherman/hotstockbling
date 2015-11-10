#!/usr/bin/env python

import os

import twilio

import config
import utils


def lambda_handler(event, context):
    body, bucket, key = utils.read_s3_from_event(event)
    recipient, sender = key.split('/')[-1].split('-')

    texter = twilio.rest.TwilioRestClient(os.environ['TWILIO_ACCOUNT_ID'], os.environ['TWILIO_AUTH_TOKEN'])
    texter.messages.create(body=body['message'], to=recipient, from_=sender)
