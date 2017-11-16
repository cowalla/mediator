from gdax import AuthenticatedClient as GDAXClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from settings import FIATS, SPLIT_CHARACTER, GDAX, LIQUI, POLONIEX


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


def sort_pair_by_fiat(currency_pair, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    currencies = currency_pair.lower().split(SPLIT_CHARACTER)

    if fiat_order is None:
        # Mediator order
        fiat_order = FIATS
    if len(currencies) != 2:
        # this function could be opened up to sort any length, if necessary
        raise NotImplementedError

    sorted_by_order = [c for _, c in sorted(zip(fiat_order, currencies))]

    return (sorted_by_order[0], sorted_by_order[1])


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
        self.currencies = sorted(self._get_currencies_from_pairs(self.pairs))

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


class LiquiClientHelper(ClientHelper):
    NAME = LIQUI
    CLIENT_CLASS = LiquiClient

    def get_ticker(self):
        all_liqui_pairs = [self._to_client_pair(p) for p in self.pairs]
        pair = ','.join(all_liqui_pairs)

        return self.client.ticker(pair=pair)

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_pairs(pairs)

    def _get_client_pairs(self):
        return self.client.info()['pairs'].keys()

    def _get_fiats_from_pairs(self, pairs):
        return set([pair[0] for pair in pairs])


class PoloniexClientHelper(ClientHelper):
    NAME = POLONIEX
    CLIENT_CLASS = PoloniexClient

    def get_currencies(self):
        return self.client.returnCurrencies().keys()

    def get_ticker(self):
        return self.client.returnTicker()

    def _get_client_pairs(self):
        return self.get_ticker().keys()


class GDAXClientHelper(ClientHelper):
    NAME = GDAX
    CLIENT_CLASS = GDAXClient

    def get_currencies(self):
        return self.client.get_info()['funds'].keys()

    def get_ticker(self):
        return self.client.ticker()

    def _get_client_pairs(self):
        return self.client.get_products()
