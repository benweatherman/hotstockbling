#!/usr/bin/env python

import twilio

import utils


def lambda_handler(event, context):
    body, bucket, key = utils.read_s3_from_event(event)
    recipient, sender = key.split('/')[-1].split('-')

    texter = twilio.rest.TwilioRestClient('AC0da4bb58cc359e247217dd0349f8e581', '8a3a8d6ac03ff5330d227cda782f3b2c')
    texter.messages.create(body=body['message'], to=recipient, from_=sender)
