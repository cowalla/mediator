import unittest
from mock import Mock, patch, create_autospec

from fixtures.liqui import info as liqui_info, ticker as liqui_ticker
from fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)


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