from copy import deepcopy
from mock import Mock

from crypto_mediator.fixtures.bittrex import (
    getmarkets as bittrex_get_markets, getmarketsummaries as bittrex_get_market_summaries
)
from crypto_mediator.fixtures.gdax import (
    currencies as gdax_currencies, products as gdax_products, ticker as gdax_ticker
)
from crypto_mediator.fixtures.liqui import info as liqui_info, ticker as liqui_ticker
from crypto_mediator.fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)

class MockClient(object):
    def __init__(self, **kwargs):
        super(MockClient, self).__init__()

class MockBittrexClient(Mock):

    def get_markets(self):
        return deepcopy(bittrex_get_markets.response)

    def get_market_summaries(self):
        return deepcopy(bittrex_get_market_summaries.response)


class MockGDAXClient(Mock):

    def get_currencies(self):
        return gdax_currencies.response

    def get_product_ticker(self, id):
        return gdax_ticker.response(id)

    def get_products(self):
        return gdax_products.response


class MockLiquiClient(Mock):

    def info(self):
        return liqui_info.response

    def ticker(self, pair):
        response = liqui_ticker.response
        pairs = pair.split('-')

        return {p: response[p] for p in pairs}


class MockPoloniexClient(Mock):

    def returnCurrencies(self):
        return poloniex_currencies.response

    def returnTicker(self):
        return poloniex_ticker.response