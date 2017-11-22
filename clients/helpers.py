from gdax import AuthenticatedClient as GDAXClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from settings import FIATS, SPLIT_CHARACTER, GDAX, LIQUI, POLONIEX


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
    a_index, b_index = get_fiat_order(a, fiat_order), get_fiat_order(b, fiat_order)

    if b_index is None:
        return a, b
    elif a_index is None:
        return b, a
    elif a_index < b_index:
        return a, b
    else:
        return b, a


def sort_pair_by_fiat(currency_pair, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    currencies = currency_pair.lower().split(SPLIT_CHARACTER)

    return sorted_by_fiat(currencies, fiat_order)

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
            self._from_client_pair(p): p
            for p in self.client_pairs
        }
        self.pairs = sorted(self.pair_map.keys())
        self.fiats = self._get_fiats_from_pairs(self.pairs)
        self.currencies = self.get_currencies()

    def get_currencies(self):
        raise NotImplementedError

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self._from_client_pair(pair) for pair in pairs]

    def _get_client_pairs(self):
        raise NotImplementedError

    def _from_client_pair(self, pair):
        # translates a pair from its format to `Mediator` format
        return sort_pair_by_fiat(pair)

    def _to_client_pair(self, pair):
        # translates a pair from `Mediator` format to its own client format
        return self.pair_map[pair]

    def _get_fiats_from_pairs(self, pairs):
        flat = flatten([pair[0] for pair in pairs])

        return list(set(flat))

    def _get_currencies_from_pairs(self, pairs):
        flat = flatten(pairs)

        return list(set(flat))

    def _to_fiat_currency(self, pair, character=None):
        if character is None:
            character = self.SPLIT_CHARACTER

        return pair.split(character)

    def mediator_pair(self, pair):
        return self.SPLIT_CHARACTER.join(sorted_by_fiat(self._to_fiat_currency(pair)))


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

        return self._get_currencies_from_pairs(pairs)

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


class GDAXClientHelper(ClientHelper):
    # unlikely to be used in the future
    NAME = GDAX
    CLIENT_CLASS = GDAXClient

    def get_currencies(self):
        return self.client.get_currencies()

    def get_ticker(self):
        return self.client.get_product_ticker()

    def _get_client_pairs(self):
        return self.client.get_products()
