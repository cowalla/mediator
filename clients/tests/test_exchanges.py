import unittest
from mock import Mock, patch, create_autospec

from clients.exchanges import (
    flatten, sort_pair_by_fiat, LiquiClientHelper, PoloniexClientHelper, GDAXClientHelper
)
from fixtures.liqui import info as liqui_info, ticker as liqui_ticker
from fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)


class TestUtils(unittest.TestCase):

    def test_flattens_list(self):
        l = [[1, 2], 3, [4, 5, 6, 7]]

        self.assertListEqual(flatten(l), range(1, 8))

    def test_sort_pair_by_fiat(self):
        pair = 'ETH_BTC'
        fiat, currency = sort_pair_by_fiat(pair)

        self.assertEqual(fiat, 'btc')
        self.assertEqual(currency, 'eth')

        FIAT_ORDER = ['best', 'second', 'last']
        pair = 'second_last'
        fiat, currency = sort_pair_by_fiat(pair, fiat_order=FIAT_ORDER)

        self.assertEqual(fiat, 'second')
        self.assertEqual(currency, 'last')


class MockLiquiClient(Mock):
    def info(self):
        return liqui_info.response

    def ticker(self, pair):
        response = liqui_ticker.response
        pairs = pair.split(',')

        return {p: response[p] for p in pairs}


class TestLiquiClient(unittest.TestCase):

    def setUp(self):
        LiquiClientHelper.CLIENT_CLASS = MockLiquiClient

        self.credentials = ['mockKey', 'mockSecret']
        self.helper = LiquiClientHelper(*self.credentials)

    def test_init(self):
        all_currencies = list(set(flatten([p.split('_') for p in liqui_ticker.pairs])))

        self.assertEqual(self.helper.client_pairs, sorted(liqui_ticker.pairs))
        self.assertIn(('usdt', 'eth'), self.helper.pairs)
        self.assertIn(('btc', 'ltc'), self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['usdt', 'eth', 'btc'])
        self.assertEqual(self.helper.currencies, all_currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn(('usdt', 'eth'), pairs)
        self.assertIn(('btc', 'ltc'), pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usdt', currencies)
        self.assertIn('btc', currencies)
        self.assertIn('omg', currencies)

    def test_get_ticker(self):
        ticker_info = self.helper.get_ticker()

        self.assertDictEqual(ticker_info, liqui_ticker.response)


class MockPoloniexClient(Mock):
    def returnCurrencies(self):
        return poloniex_currencies.response

    def returnTicker(self):
        return poloniex_ticker.response


class TestPoloniexClient(unittest.TestCase):

    def setUp(self):
        PoloniexClientHelper.CLIENT_CLASS = MockPoloniexClient

        self.credentials = ['mockKey', 'mockSecret']
        self.helper = PoloniexClientHelper(*self.credentials)

        self.client_pairs = poloniex_ticker.response.keys()
        self.currencies = [k.lower() for k in poloniex_currencies.response.keys()]

    def test_init(self):
        client_pairs = poloniex_ticker.response.keys()
        self.assertEqual(self.helper.client_pairs, sorted(client_pairs))
        self.assertIn(('usdt', 'eth'), self.helper.pairs)
        self.assertIn(('btc', 'ltc'), self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['ltc', 'zec', 'dash', 'xmr', 'btc', 'eth', 'usdt'])
        self.assertEqual(self.helper.currencies, self.currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn(('usdt', 'eth'), pairs)
        self.assertIn(('btc', 'ltc'), pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usdt', currencies)
        self.assertIn('btc', currencies)
        self.assertIn('omg', currencies)

    def test_get_ticker(self):
        ticker_info = self.helper.get_ticker()

        self.assertDictEqual(ticker_info, poloniex_ticker.response)


