#!/usr/bin/env python

import json
import re
import textwrap

import config
import stock_api
import utils
from lager import logger


def lambda_handler(event, context):
    utils.log_lambda(event, context)

    body, bucket, _ = utils.read_s3_from_event(event)

    message = body['Body']
    stocks = re.split(r'\W+', message)

    for stock in stocks:
        if stock == 'overview':
            continue

        stock_info = {}
        try:
            stock_info = stock_api.get_info(stock)
            message = format_ticker_message(stock_info)
        except Exception as e:
            logger.exception('Could not get stock ticker info')
            message = str(e)

        recipient = body['From']
        sender = body['To']

        utils.send_sms(message, sender, recipient, bucket)

        if stock_info:
            key = 'parsed-overview/{}-{}-{}'.format(recipient, stock_info['Symbol'], body['MessageSid'])
            config.S3_CLIENT.put_object(Bucket=bucket, Key=key, Body=json.dumps(body))


def format_ticker_message(info):
    msg = '''
        {symbol} @ ${current}
    '''.format(symbol=info['Symbol'], current=info['LastPrice'])
    msg = textwrap.dedent(msg).strip()

    return msg
