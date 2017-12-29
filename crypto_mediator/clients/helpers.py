from bittrex.bittrex import Bittrex as BittrexClient
from gdax import PublicClient as GDAXClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from crypto_mediator.settings import FIATS, MEDIATOR_SPLIT_CHARACTER, BITTREX, GATECOIN, GDAX, LIQUI, POLONIEX
from crypto_mediator.clients.gatecoin import GatecoinClient


class ClientError(AttributeError):
    pass


def flatten(l):
    # flattens a list one level
    flattened = []

    for item in l:
        if isinstance(item, list):
            flattened += item
        elif isinstance(item, tuple):
            flattened += list(item)
        else:
            flattened.append(item)

    return flattened


def get_fiat_order(f, fiat_order):
    try:
        return fiat_order.index(f)
    except ValueError:
        # not in fiat_order
        return None


def rename_keys(data, map):
    return {
        local_key: data[client_key]
        for client_key, local_key in map.iteritems()
        if data.get(client_key) is not None
    }


def sorted_by_fiat(currencies, fiat_order=None):
    if fiat_order is None:
        # Mediator order
        fiat_order = FIATS
    if len(currencies) != 2:
        # this function could be opened up to sort any length, if necessary
        raise NotImplementedError

    [a, b] = currencies
    a = a.lower()
    b = b.lower()
    a_index, b_index = get_fiat_order(a, fiat_order), get_fiat_order(b, fiat_order)

    if b_index is None:
        return a, b
    elif a_index is None:
        return b, a
    elif a_index < b_index:
        return a, b
    else:
        return b, a


def sort_pair_by_fiat(currency_pair, split_character=None, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    if split_character is None:
        split_character = MEDIATOR_SPLIT_CHARACTER

    currencies = currency_pair.split(split_character)
    sorted_pair = sorted_by_fiat(currencies, fiat_order)

    return MEDIATOR_SPLIT_CHARACTER.join(sorted_pair)

class ClientHelper(object):
    NAME = None
    CLIENT_CLASS = None
    SPLIT_CHARACTER = '_'

    def __init__(self, *args, **kwargs):
        super(ClientHelper, self).__init__()

        self.fiats = set()
        self.pairs = []
        self.currencies = []

        self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        self.client = self.CLIENT_CLASS(*args, **kwargs)

        self.client_pairs = sorted(self._get_client_pairs())
        self.pair_map = {
            self.mediator_pair(p): p
            for p in self.client_pairs
        }
        self.pairs = sorted(self.pair_map.keys())
        self.fiats = self._get_fiats_from_mediator_pairs(self.pairs)
        self.currencies = self.get_currencies()

    def get_currencies(self):
        raise NotImplementedError

    def trade_history(self):
        raise NotImplementedError

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self.mediator_pair(pair) for pair in pairs]

    def _get_client_pairs(self):
        raise NotImplementedError

    def _to_client_pair(self, pair):
        # translates a pair from `Mediator` format to its own client format
        return self.pair_map[pair]

    def _get_fiats_from_mediator_pairs(self, pairs):
        fiats = set([pair.split(MEDIATOR_SPLIT_CHARACTER)[0] for pair in pairs])

        return list(fiats)

    def _get_currencies_from_mediator_pairs(self, pairs):
        flat = flatten([pair.split(MEDIATOR_SPLIT_CHARACTER) for pair in pairs])

        return list(set(flat))

    def mediator_pair(self, pair):
        fiat_currency = pair.split(self.SPLIT_CHARACTER)

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))


class BittrexClientHelper(ClientHelper):
    """
    client ticker keys:
        [
            u'PrevDay',
            u'Volume',
            u'Last',
            u'OpenSellOrders',
            u'TimeStamp',
            u'Bid',
            u'Created',
            u'OpenBuyOrders',
            u'High',
            u'MarketName',
            u'Low',
            u'Ask',
            u'BaseVolume',
        ]
    """
    TICKER_MAP = {
        'Last': 'last',
        'Bid': 'highest_bid',
        'Ask': 'lowest_ask',
        'BaseVolume': 'base_volume',
        'Volume': 'current_volume',
        'High': 'high',
        'Low': 'low',
        'TimeStamp': 'updated',
    }

    NAME = BITTREX
    CLIENT_CLASS = BittrexClient
    SPLIT_CHARACTER = '-'

    def get_ticker(self):
        ticker_response = self.client.get_market_summaries()

        if not ticker_response['success']:
            raise ClientError(ticker_response['message'])

        ticker = {}

        for entry in ticker_response['result']:
            client_pair = entry.pop('MarketName')
            mediator_pair = self.mediator_pair(client_pair)

            ticker[mediator_pair] = rename_keys(entry, self.TICKER_MAP)

        return ticker

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    def get_pairs(self):
        client_pairs = self._get_client_pairs()

        return [
            self.mediator_pair(pair)
            for pair in client_pairs
        ]

    def _get_client_pairs(self):
        markets_response = self.client.get_markets()

        return [
            self.SPLIT_CHARACTER.join([r['BaseCurrency'], r['MarketCurrency']])
            for r in markets_response['result']
        ]

class GatecoinClientHelper(ClientHelper):
    NAME = GATECOIN
    CLIENT_CLASS = GatecoinClient
    SPLIT_CHARACTER = ''

    TICKER_MAP = {
        'last': 'last',
        'bid': 'highest_bid',
        'ask': 'lowest_ask',
        'volume': 'base_volume',
        'high': 'high',
        'low': 'low',
        'createDateTime': 'updated',
        'vwap': 'average',
    }

    def mediator_pair(self, pair):
        # I hate you gatecoin
        fiat = pair[:len(pair)/2]
        currency = pair[len(pair)/2:]
        fiat_currency = [fiat, currency]

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))

    def _get_client_pairs(self):
        return [t['currencyPair'] for t in self.client.livetickers().get('tickers')]

    def get_currencies(self, use_cache=True):
        self.pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(self.pairs)

    def get_ticker(self):
        response = self.client.livetickers().get('tickers')

        if not response:
            print response
            raise ClientError('No response from Gatecoin.')

        ticker = {}

        for currency_ticker in response:
            client_pair = currency_ticker['currencyPair']
            mediator_pair = self.mediator_pair(client_pair)
            ticker[mediator_pair] = rename_keys(currency_ticker, self.TICKER_MAP)

        return ticker


class GDAXClientHelper(ClientHelper):
    # unlikely to be used in the future
    NAME = GDAX
    CLIENT_CLASS = GDAXClient
    TICKER_MAP = {
        'bid': 'highest_bid',
        'ask': 'lowest_ask',
        'volume': 'current_volume',
        'time': 'updated',
        'price': 'price',
    }
    SPLIT_CHARACTER = '-'

    def get_currencies(self):
        return [p['id'].lower() for p in self.client.get_currencies()]

    def get_ticker(self):
        raise NotImplementedError('API does not allow polling for all pairs')

    def get_product_ticker(self, pair):
        client_pair = self.pair_map[pair]
        response = self.client.get_product_ticker(client_pair)

        return rename_keys(response, self.TICKER_MAP)

    def _get_client_pairs(self):
        return [p['id'] for p in self.client.get_products()]


class LiquiClientHelper(ClientHelper):
    TICKER_MAP = {
        'last': 'last',
        'buy': 'highest_bid',
        'sell': 'lowest_ask',
        'vol': 'base_volume',
        'vol_cur': 'current_volume',
        'high': 'high',
        'low': 'low',
        'updated': 'updated',
        'avg': 'average',
    }

    NAME = LIQUI
    CLIENT_CLASS = LiquiClient

    # public methods

    def get_ticker(self):
        all_liqui_pairs = [self._to_client_pair(p) for p in self.pairs]
        pair = '-'.join(all_liqui_pairs)
        ticker_response = self.client.ticker(pair=pair)

        if ticker_response.get('error'):
            raise ClientError(ticker_response['error'])

        return {
            self.mediator_pair(pair): rename_keys(data, self.TICKER_MAP)
            for pair, data in ticker_response.iteritems()
        }

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    # account information

    def trade_history(self):
        response = self.client.trade_history()
        trades = response.values()

        for trade in trades:
            trade['pair'] = self.mediator_pair(trade['pair'])

        return sorted(trades, key=lambda x: x['timestamp'])

    def _get_client_pairs(self):
        return self.client.info()['pairs'].keys()


class PoloniexClientHelper(ClientHelper):
    TICKER_MAP = {
        'id': 'id',
        'last': 'last',
        'lowestAsk': 'lowest_ask',
        'highestBid': 'highest_bid',
        'percentChange': 'percent_change',
        'baseVolume': 'base_volume',
        'quoteVolume': 'quote_volume',
        'isFrozen': 'is_frozen',
        'high24hr': 'high',
        'low24hr': 'low',
    }

    NAME = POLONIEX
    CLIENT_CLASS = PoloniexClient

    def get_currencies(self):
        return self.client.returnCurrencies().keys()

    def get_ticker(self):
        ticker_response = self.client.returnTicker()

        return {
            self.mediator_pair(pair): rename_keys(data, self.TICKER_MAP)
            for pair, data in ticker_response.iteritems()
        }

    def _get_client_pairs(self):
        return self.get_ticker().keys()
