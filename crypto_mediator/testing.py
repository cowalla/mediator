from copy import deepcopy
from mock import Mock

from crypto_mediator.fixtures.bittrex import (
    getmarkets as bittrex_get_markets, getmarketsummaries as bittrex_get_market_summaries
)
from crypto_mediator.fixtures.gatecoin import livetickers as gatecoin_livetickers
from crypto_mediator.fixtures.gdax import (
    currencies as gdax_currencies,
    products as gdax_products,
    rates as gdax_rates,
    ticker as gdax_ticker,
)
from crypto_mediator.fixtures.liqui import info as liqui_info, ticker as liqui_ticker
from crypto_mediator.fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)

class MockClient(Mock):
    def get_accounts(self):
        return [
            {'currency': 'eth', 'address': '0xhfjskahfjakshdsjkh'},
        ]


class MockBittrexClient(MockClient):

    def get_markets(self):
        return deepcopy(bittrex_get_markets.response)

    def get_market_summaries(self):
        return deepcopy(bittrex_get_market_summaries.response)


class MockGatecoinClient(MockClient):

    def livetickers(self):
        return gatecoin_livetickers.response


class MockGDAXClient(MockClient):

    def get_currencies(self):
        return gdax_currencies.response

    def get_product_ticker(self, id):
        return gdax_ticker.response(id)

    def get_products(self):
        return gdax_products.response

    def get_product_historic_rates(self, product_id, **kwargs):
        return gdax_rates.response(product_id, **kwargs)


class MockLiquiClient(MockClient):

    def info(self):
        return liqui_info.response

    def ticker(self, pair):
        response = liqui_ticker.response
        pairs = pair.split('-')

        return {p: response[p] for p in pairs}


class MockPoloniexClient(MockClient):

    def returnCurrencies(self):
        return poloniex_currencies.response

    def returnTicker(self):
        return poloniex_ticker.response