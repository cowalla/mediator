from mock import patch
import unittest

from crypto_mediator.clients.helpers import (
    flatten, rename_keys, sort_pair_by_fiat, BittrexClientHelper, GatecoinClientHelper, GDAXClientHelper,
    LiquiClientHelper, PoloniexClientHelper,
)
from crypto_mediator.fixtures.liqui import ticker as liqui_ticker
from crypto_mediator.fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)

from crypto_mediator.testing import (
    MockBittrexClient, MockGatecoinClient, MockGDAXClient, MockLiquiClient, MockPoloniexClient,
)


class TestUtils(unittest.TestCase):

    def test_flattens_list(self):
        l = [[1, 2], 3, [4, 5, 6, 7]]

        self.assertListEqual(flatten(l), range(1, 8))

    def test_sort_pair_by_fiat(self):
        pair = 'ETH_BTC'
        sorted_pair = sort_pair_by_fiat(pair)

        self.assertEqual(sorted_pair, 'btc_eth')

        FIAT_ORDER = ['best', 'second', 'last']
        pair = 'second_last'
        sorted_pair = sort_pair_by_fiat(pair, fiat_order=FIAT_ORDER)

        self.assertEqual(sorted_pair, 'second_last')

    def test_rename_keys(self):
        data = {
            'price': 1234,
            'sell': 1235,
            'buy': 1233,
        }
        map = {
            'price': 'average_price',
            'sell': 'average_sell',
            'buy': 'average_buy',
        }

        self.assertDictEqual(
            rename_keys(data, map),
            {
                'average_price': 1234,
                'average_sell': 1235,
                'average_buy': 1233,
            }
        )


class TestBittrexClient(unittest.TestCase):

    @patch.object(BittrexClientHelper, 'CLIENT_CLASS', MockBittrexClient)
    def setUp(self):
        self.credentials = {'api_key': None, 'api_secret': None}
        self.helper = BittrexClientHelper(**self.credentials)

    def test_init(self):
        self.assertIn('usdt_eth', self.helper.pairs)
        self.assertIn('btc_ltc', self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['usdt', 'eth', 'btc'])
        self.assertIn('omg', self.helper.currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn('usdt_eth', pairs)
        self.assertIn('btc_ltc', pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usdt', currencies)
        self.assertIn('btc', currencies)
        self.assertIn('omg', currencies)

    def test_get_ticker(self):
        ticker_info = self.helper.get_ticker()
        keys = [
            'last',
            'lowest_ask',
            'highest_bid',
            'base_volume',
            'current_volume',
            'high',
            'low',
            'updated',
        ]
        self.assertIn('btc_omg', ticker_info)
        ticker_example = ticker_info['btc_omg']

        self.assertListEqual(sorted(ticker_example.keys()), sorted(keys))


class TestGatecoinClient(unittest.TestCase):

    @patch.object(GatecoinClientHelper, 'CLIENT_CLASS', MockGatecoinClient)
    def setUp(self):
        self.credentials = {}
        self.helper = GatecoinClientHelper(**self.credentials)

    def test_init(self):
        self.assertIn('usd_eth', self.helper.pairs)
        self.assertIn('btc_ltc', self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['ltc', 'eth', 'usd', 'btc'])
        self.assertIn('ltc', self.helper.currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn('usd_eth', pairs)
        self.assertIn('btc_ltc', pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usd', currencies)
        self.assertIn('btc', currencies)

    def test_get_ticker(self):
        ticker = self.helper.get_ticker()
        keys = [
            'last',
            'lowest_ask',
            'highest_bid',
            'base_volume',
            'high',
            'low',
            'updated',
            'average',
        ]
        self.assertIn('btc_rep', ticker)
        ticker_example = ticker['btc_rep']

        self.assertListEqual(sorted(ticker_example.keys()), sorted(keys))


class TestGDAXClient(unittest.TestCase):

    @patch.object(GDAXClientHelper, 'CLIENT_CLASS', MockGDAXClient)
    def setUp(self):
        self.credentials = {}
        self.helper = GDAXClientHelper(**self.credentials)

    def test_init(self):
        self.assertIn('usd_eth', self.helper.pairs)
        self.assertIn('btc_ltc', self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['ltc', 'eth', 'usd', 'btc'])
        self.assertIn('ltc', self.helper.currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn('usd_eth', pairs)
        self.assertIn('btc_ltc', pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usd', currencies)
        self.assertIn('btc', currencies)

    def test_get_product_ticker(self):
        btc_eth_ticker = self.helper.get_product_ticker('btc_eth')

        self.assertDictEqual(
            btc_eth_ticker,
            {
                'highest_bid': '0.05396',
                'lowest_ask': '0.05397',
                'current_volume': '62778.70074449',
                'updated': '2017-11-25T20:55:50.641000Z'
            }
        )

    def test_get_ticker(self):
        with self.assertRaises(NotImplementedError):
            self.helper.get_ticker()


class TestLiquiClient(unittest.TestCase):

    @patch.object(LiquiClientHelper, 'CLIENT_CLASS', MockLiquiClient)
    def setUp(self):
        self.credentials = ['mockKey', 'mockSecret']
        self.helper = LiquiClientHelper(*self.credentials)

    def test_init(self):
        all_currencies = list(set(flatten([p.split('_') for p in liqui_ticker.pairs])))

        self.assertEqual(self.helper.client_pairs, sorted(liqui_ticker.pairs))
        self.assertIn('usdt_eth', self.helper.pairs)
        self.assertIn('btc_ltc', self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['usdt', 'eth', 'btc'])
        self.assertEqual(self.helper.currencies, all_currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn('usdt_eth', pairs)
        self.assertIn('btc_ltc', pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('usdt', currencies)
        self.assertIn('btc', currencies)
        self.assertIn('omg', currencies)

    def test_get_ticker(self):
        ticker_info = self.helper.get_ticker()
        keys = [
            'last',
            'lowest_ask',
            'highest_bid',
            'base_volume',
            'current_volume',
            'high',
            'low',
            'updated',
            'average',
        ]
        self.assertIn('btc_omg', ticker_info)
        ticker_example = ticker_info['btc_omg']

        self.assertListEqual(sorted(ticker_example.keys()), sorted(keys))


class TestPoloniexClient(unittest.TestCase):

    @patch.object(PoloniexClientHelper, 'CLIENT_CLASS', MockPoloniexClient)
    def setUp(self):
        self.credentials = ['mockKey', 'mockSecret']
        self.helper = PoloniexClientHelper(*self.credentials)

        self.client_pairs = poloniex_ticker.response.keys()
        self.currencies = poloniex_currencies.response.keys()

    def test_init(self):
        self.assertIn('usdt_eth', self.helper.pairs)
        self.assertIn('btc_ltc', self.helper.pairs)

        self.assertListEqual(self.helper.fiats, ['ltc', 'zec', 'dash', 'xmr', 'btc', 'eth', 'usdt'])
        self.assertIn('ETC', self.helper.currencies)

    def test_get_pairs(self):
        pairs = self.helper.get_pairs()

        self.assertIn('usdt_eth', pairs)
        self.assertIn('btc_ltc', pairs)

    def test_get_currencies(self):
        currencies = self.helper.get_currencies()

        self.assertIn('USDT', currencies)
        self.assertIn('BTC', currencies)
        self.assertIn('OMG', currencies)

    def test_get_ticker(self):
        ticker_info = self.helper.get_ticker()
        keys = [
            'id',
            'last',
            'lowest_ask',
            'highest_bid',
            'percent_change',
            'base_volume',
            'quote_volume',
            'is_frozen',
            'high',
            'low',
        ]

        # should exist
        self.assertIn('btc_bcn', ticker_info)
        ticker_example = ticker_info['btc_bcn']
        self.assertListEqual(sorted(ticker_example.keys()), sorted(keys))
