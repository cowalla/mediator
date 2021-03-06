from mock import patch
from unittest import TestCase

from crypto_mediator.clients.client import downcased, MetaClient
from crypto_mediator.clients.helpers import (
    BittrexClientHelper, GatecoinClientHelper, CoinbaseProClientHelper, LiquiClientHelper, PoloniexClientHelper
)
from crypto_mediator.testing import (
    MockBittrexClient, MockGatecoinClient, MockCoinbaseProClient, MockLiquiClient, MockPoloniexClient,
)


class TestDowncased(TestCase):

    def test_lowercases_data(self):
        my_string = 'aBc 1234 $@!#'
        downcase = downcased(my_string)

        self.assertEqual(downcase, my_string.lower())


class TestMetaClient(TestCase):

    @patch.object(BittrexClientHelper, 'CLIENT_CLASS', MockBittrexClient)
    @patch.object(GatecoinClientHelper, 'CLIENT_CLASS', MockGatecoinClient)
    @patch.object(CoinbaseProClientHelper, 'CLIENT_CLASS', MockCoinbaseProClient)
    @patch.object(LiquiClientHelper, 'CLIENT_CLASS', MockLiquiClient)
    @patch.object(PoloniexClientHelper, 'CLIENT_CLASS', MockPoloniexClient)
    def setUp(self):
        self.maxDiff = None
        self.kwargs = {
            'liqui': {'key': 'key', 'secret': 'secret'},
            'poloniex': {'key': 'key', 'secret': 'secret'},
            'bittrex': {'api_key': 'key', 'api_secret': 'secret'},
            'coinbasepro': {'key': 'key', 'b64secret': 'b64secret', 'passphrase': 'mypassword'},
            'gatecoin': {'key': 'key', 'secret': 'secret'},
        }
        self.client = MetaClient(**self.kwargs)

    def test_init(self):
        self.assertEqual(len(self.client.helpers), 5)

    @patch.object(BittrexClientHelper, 'CLIENT_CLASS', MockBittrexClient)
    @patch.object(GatecoinClientHelper, 'CLIENT_CLASS', MockGatecoinClient)
    @patch.object(CoinbaseProClientHelper, 'CLIENT_CLASS', MockCoinbaseProClient)
    @patch.object(LiquiClientHelper, 'CLIENT_CLASS', MockLiquiClient)
    @patch.object(PoloniexClientHelper, 'CLIENT_CLASS', MockPoloniexClient)
    def test_init_unsupported_exchange(self):
        self.kwargs['unsupported'] = {}

        with self.assertRaisesRegexp(NotImplementedError, 'unsupported is not implemented!'):
            MetaClient(**self.kwargs)

    def test_bittrex_ticker(self):
        btc_1st = {
            'last': 0.00004692,
            'lowest_ask': 0.00004691,
            'highest_bid': 0.00004633,
            'base_volume': 106.56404429,
            'current_volume': 2241173.71259967,
            'high': 0.00004996,
            'low': 0.00004201,
            'updated': 1511412109.0,
        }
        self.assertDictEqual(
            btc_1st,
            self.client.ticker('bittrex')['btc_1st']
        )

    def test_gatecoin_ticker(self):
        ticker = self.client.ticker('gatecoin')

        btc_rep = ticker['btc_rep']
        self.assertDictEqual(
            btc_rep,
            {
                'average': 0.0,
                'last': 0.002775,
                'lowest_ask': 0.029979,
                'highest_bid': 0.00051,
                'base_volume': 0.0,
                'high': 0.002775,
                'low': 0.002775,
                'updated': 1511813522.0,
            }
        )

    def test_coinbasepro_ticker(self):
        with self.assertRaises(NotImplementedError):
            self.client.ticker('coinbasepro')

        eth_btc = self.client.product_ticker('coinbasepro', 'btc_eth')
        self.assertDictEqual(
            eth_btc,
            {
                'current_volume': 62778.70074449,
                'highest_bid': 0.05396,
                'lowest_ask': 0.05397,
                'price': 0.05397,
                'updated': 1511679350.0,
            }
        )

    def test_liqui_ticker(self):
        bmc_usdt = {
            'last': 0.6220695,
            'lowest_ask': 0.62508059,
            'highest_bid': 0.61905832,
            'base_volume': 81296.8647402806507957,
            'current_volume': 131309.57718612,
            'high': 0.64828129,
            'low': 0.58545808,
            'updated': 1510788150,
            'average': 0.616869685,
        }
        self.assertDictEqual(
            bmc_usdt,
            self.client.ticker('liqui')['usdt_bmc']
        )

    def test_poloniex_ticker(self):
        btc_bcn = {
            'id': 7,
            'last': 0.00000017,
            'lowest_ask': 0.00000017,
            'highest_bid': 0.00000016,
            'percent_change': 0.00000000,
            'base_volume': 26.85861414,
            'quote_volume': 163214330.95054007,
            'is_frozen': 0,
            'high': 0.00000018,
            'low': 0.00000016,
        }
        data = self.client.ticker('poloniex')
        self.assertDictEqual(
            btc_bcn,
            data['btc_bcn']
        )

    def test_bittrex_pairs(self):
        pair = 'btc_ltc'
        data = self.client.pairs('bittrex')

        self.assertIn(pair, data)

    def test_gatecoin_pairs(self):
        pair = 'btc_ltc'
        data = self.client.pairs('gatecoin')

        self.assertIn(pair, data)

    def test_coinbasepro_pairs(self):
        pair = 'btc_ltc'
        data = self.client.pairs('coinbasepro')

        self.assertIn(pair, data)

    def test_liqui_pairs(self):
        pair = 'btc_ltc'
        data = self.client.pairs('liqui')

        self.assertIn(pair, data)

    def test_poloniex_pairs(self):
        pair = 'btc_ltc'
        data = self.client.pairs('poloniex')

        self.assertIn(pair, data)
