#!/usr/bin/env python

import requests

from lager import logger

LOOKUP_API_URL = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json'
QUOTE_API_URL = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json'


def get_info(stock):
    try:
        return get_ticker_info(stock)
    except:
        companies = lookup_company(stock)

        if len(companies) == 0:
            raise Exception('Unable to find info for "{}"'.format(stock))

        tickers = set([company['symbol'].lower() for company in companies])
        if stock.lower() in tickers:
            ticker = next(company['symbol'] for company in companies if company['symbol'].lower() == stock)
            return get_ticker_info(ticker)

        msg = '"{}" is ambiguous. Did you mean one of these?\n'.format(stock)
        options = ['{} {}'.format(d['symbol'], d['name']) for d in companies]
        msg += '\n'.join(options)
        raise Exception(msg)


def lookup_company(company):
    params = {'input': company}

    resp = requests.get(LOOKUP_API_URL, data=params, timeout=10)
    logger.info(resp.url)
    logger.info(resp.status_code)
    logger.info(resp.headers)
    logger.info(resp.text)

    # The stocks API doesn't actually return a failing status code, but we'll keep
    # this here in case there are network problems, etc.
    if not resp.ok:
        raise Exception('Unable to find info for "{}"'.format(company))

    # Sometimes the same stock is listed on multiple exchanges. We can ignore those for the sake of this prototype.
    results = set((d['Symbol'], d['Name']) for d in resp.json())

    return [{'symbol': symbol, 'name': name} for symbol, name in results]


def get_ticker_info(ticker):
    params = {'symbol': ticker}

    resp = requests.get(QUOTE_API_URL, data=params, timeout=10)
    logger.info(resp.url)
    logger.info(resp.status_code)
    logger.info(resp.headers)
    logger.info(resp.text)

    # The stocks API doesn't actually return a failing status code, but we'll keep
    # this here in case there are network problems, etc.
    if not resp.ok:
        raise Exception('Unable to find a symbol for "{}"'.format(ticker))
    # This is how the stocks API responds when there's an error, they always report
    # a 200 status code
    elif 'Message' in resp.json():
        raise Exception('Unable to find a symbol for "{}"'.format(ticker))

    return resp.json()
