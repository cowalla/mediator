from mock import patch
import unittest

from crypto_mediator.clients.helpers.helper import flatten, rename_keys_values, sort_pair_by_fiat
from crypto_mediator.clients.helpers import (
    BittrexClientHelper, GatecoinClientHelper, CoinbaseProClientHelper,
    LiquiClientHelper, PoloniexClientHelper,
)
from crypto_mediator.fixtures.liqui import ticker as liqui_ticker
from crypto_mediator.fixtures.poloniex import (
    returnCurrencies as poloniex_currencies, returnTicker as poloniex_ticker
)

from crypto_mediator.testing import (
    MockBittrexClient, MockGatecoinClient, MockCoinbaseProClient, MockLiquiClient, MockPoloniexClient,
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

    def test_rename_keys_values(self):
        data = {
            'price': 1234,
            'sell': 1235,
            'buy': 1233,
        }
        key_map = {
            'price': 'average_price',
            'sell': 'average_sell',
            'buy': 'average_buy',
        }
        value_types = {
            'price': int,
            'sell': str,
            'buy': float,
        }

        self.assertDictEqual(
            rename_keys_values(data, key_map, value_types),
            {
                'average_price': 1234,
                'average_sell': str(1235),
                'average_buy': float(1233),
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
        ticker = self.helper.get_ticker()
        self.assertNotEqual(len(ticker), 0)


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
        self.assertNotEqual(len(ticker), 0)


class TestCoinbaseProClient(unittest.TestCase):

    @patch.object(CoinbaseProClientHelper, 'CLIENT_CLASS', MockCoinbaseProClient)
    def setUp(self):
        self.credentials = {'key': 'key', 'b64secret': 'b64secret', 'passphrase': 'mypassword'}
        self.helper = CoinbaseProClientHelper(**self.credentials)

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
        self.assertIsNotNone(btc_eth_ticker)

    def test_get_ticker(self):
        with self.assertRaises(NotImplementedError):
            self.helper.get_ticker()

    def test_get_historic_rates(self):
        eth_usd_rates = self.helper.get_rates('usd_eth')
        initial_rate, final_rate = eth_usd_rates[0], eth_usd_rates[-1]

        self.assertDictEqual(
            initial_rate,
            {'close': 1087,
             'high': 1087,
             'low': 1086.99,
             'open': 1087,
             'timestamp': 1517068620,
             'volume': 9.74795564}
        )
        self.assertDictEqual(
            final_rate,
            {'close': 1104.99,
             'high': 1104.99,
             'low': 1104.98,
             'open': 1104.99,
             'timestamp': 1517089620,
             'volume': 10.5441164}
        )


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

        self.assertListEqual(sorted(self.helper.fiats), sorted(['usdt', 'eth', 'btc']))
        self.assertEqual(sorted(self.helper.currencies), sorted(all_currencies))

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
        self.assertIn('omg_btc', ticker_info)


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

        self.assertListEqual(sorted(self.helper.fiats), sorted(['ltc', 'zec', 'dash', 'xmr', 'btc', 'eth', 'usdt']))
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
        self.assertIn('BTC_BCN', ticker_info)
