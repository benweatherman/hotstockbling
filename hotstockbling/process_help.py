#!/usr/bin/env python

import utils


def lambda_handler(event, context):
    utils.log_lambda(event, context)

    body, bucket, _ = utils.read_s3_from_event(event)

    recipient = body['From']
    sender = body['To']

    message = 'Thanks for using hotstockbling. Enter a ticker symbol or use HELPME, DETAILS, BUY, or SELL.'
    utils.send_sms(message, sender, recipient, bucket)
