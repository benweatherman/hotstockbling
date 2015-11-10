#!/usr/bin/env python

import json
import re
from collections import defaultdict

import config
import utils
from stock_api import get_info


def lambda_handler(event, context):
    utils.log_lambda(event, context)

    body, bucket, _ = utils.read_s3_from_event(event)

    message = body['Body']
    cmd, ticker, count = re.split('\W+', message)

    stock_info = get_info(ticker)
    symbol = stock_info['Symbol']
    current_price = stock_info['LastPrice']

    recipient = body['From']

    portfolio_key = 'portfolio/{}.json'.format(recipient)
    try:
        portfolio = utils.read_s3(bucket, portfolio_key)
        current_portfolio = defaultdict(list, portfolio)
    except:
        current_portfolio = defaultdict(list)

    current_portfolio[symbol].append({'count': -1 * int(count), 'price': current_price})

    config.S3_CLIENT.put_object(Bucket=bucket, Key=portfolio_key, Body=json.dumps(current_portfolio))

    total_shares = sum(int(d['count']) for d in current_portfolio[symbol])

    sender = body['To']
    message = 'You sold {} shares of {} @ ${}. You have a total of {} shares.'.format(count, symbol, current_price, total_shares)
    utils.send_sms(message, sender, recipient, bucket)
