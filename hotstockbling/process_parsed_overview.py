#!/usr/bin/env python

import collections
import json

import requests

import utils
import config
from lager import logger

import os
GECKOBOARD_API_KEY = os.environ.get('GECKOBOARD_API_KEY')


def send_stock_overview(data):
    tickers = [d[0] for d in data]
    counter = collections.Counter(tickers)

    analytics_data = [{'value': count, 'label': ticker} for ticker, count in counter.most_common()]
    request_data = {
        'api_key': GECKOBOARD_API_KEY,
        'data': {
            'item': analytics_data
        }
    }

    logger.info('Sending data to geckoboard')
    logger.info(json.dumps(request_data, indent=2))

    resp = requests.post('https://push.geckoboard.com/v1/send/166608-edb468d1-bea2-41fe-ae36-e45b326128aa', json=request_data)
    resp.raise_for_status()


def send_phone_leaderboard(data):
    tickers = [d[1] for d in data]
    counter = collections.Counter(tickers)

    analytics_data = [{'value': count, 'label': ticker} for ticker, count in counter.most_common()]
    request_data = {
        'api_key': GECKOBOARD_API_KEY,
        'data': {
            'items': analytics_data
        }
    }

    logger.info('Sending data to geckoboard')
    logger.info(json.dumps(request_data, indent=2))

    resp = requests.post('https://push.geckoboard.com/v1/send/166608-0e9d28b7-40df-40db-959a-bba383c84ec3', json=request_data)
    resp.raise_for_status()


def get_parsed_data(bucket, prefix):
    resp = config.S3_CLIENT.list_objects(Bucket=bucket, Prefix=prefix)
    logger.info('parsed overview files')
    logger.info(resp)

    files = resp.get('Contents', [])

    return [f['Key'].replace(prefix, '').split('-')[:2] for f in files]


def analyze(bucket):
    data = get_parsed_data(bucket, 'parsed-overview/')
    logger.info('beautiful stock data')
    logger.info(data)
    send_stock_overview(data)
    send_phone_leaderboard(data)


def lambda_handler(event, context):
    utils.log_lambda(event, context)

    bucket = event['Records'][0]['s3']['bucket']['name']
    analyze(bucket)


if __name__ == '__main__':
    analyze(config.S3_MESSAGE_BUCKET)
