from gdax import AuthenticatedClient as GDAXClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from settings import FIATS, SPLIT_CHARACTER


def flatten(l):
    return [item for sublist in l for item in sublist]


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
    SPLIT_CHARACTER = '_'

    def __init__(self):
        super(ClientHelper, self).__init__()

        self.fiats = set()
        self.pairs = []
        self.currencies = []

        self.initialize()

    def initialize(self):
        self.pairs = self._client_get_pairs()
        self.fiats = self._get_fiats_from_pairs(self.pairs)
        self.currencies = self._get_currencies_from_pairs(self.pairs)

    def _client_get_pairs(self):
        raise NotImplementedError

    def _from_client_pair(self, pair):
        # translates a pair from its format to `Mediator` format
        return sort_pair_by_fiat(pair)

    def _to_client_pair(self, pair):
        # translates a pair from `Mediator` format to its own client format
        raise NotImplementedError

    def _get_fiats_from_pairs(self, pairs):
        return set([self._to_fiat_currency(pair)[0] for pair in pairs])

    def _get_currencies_from_pairs(self, pairs):
        return set([flatten(self._to_fiat_currency(pair)) for pair in pairs])

    def _to_fiat_currency(self, pair, character=None):
        if character is None:
            character = self.SPLIT_CHARACTER

        return pair.split(character)


class LiquiClientHelper(ClientHelper):
    def __init__(self, **credentials):
        self.client = LiquiClient(**credentials)

        super(LiquiClientHelper, self).__init__()

    def initialize(self):
        self.pairs = self._client_get_pairs()
        self.fiats = self._get_fiats_from_pairs(self.pairs)
        self.currencies = self._get_currencies_from_pairs(self.pairs)

    def get_ticker(self):
        liqui_pairs = [self._to_client_pair(p) for p in self.pairs]

        return self.client.ticker(pair=','.join(liqui_pairs))

    def get_currencies(self):
        pairs = self.get_pairs()

        return list(set([flatten(self._to_fiat_currency(pair)) for pair in pairs]))

    def get_pairs(self):
        pairs = self._client_get_pairs()

        return [self._from_client_pair(pair) for pair in pairs]

    def _client_get_pairs(self):
        return self.client.info()['pairs'].keys()

    def _to_client_pair(self, pair):
        [fiat, currency] = self._to_fiat_currency(pair)

        if fiat in self.fiats:
            return pair

        return self.SPLIT_CHARACTER.join([currency, fiat])


class PoloniexClientHelper(ClientHelper):
    def __init__(self, **credentials):
        self.client = PoloniexClient(**credentials)

        super(PoloniexClientHelper, self).__init__()

    def get_currencies(self):
        return self.client.returnCurrencies().keys()

    def get_ticker(self):
        return self.client.returnTicker()

    def get_pairs(self):
        pairs = self.get_ticker().keys()

        return [self._from_client_pair(pair) for pair in pairs]

    def _client_get_pairs(self):
        return self.client.returnTicker().keys()

    def _to_client_pair(self, pair):
        [fiat, currency] = self._to_fiat_currency(pair)

        if fiat in self.fiats:
            return pair

        return self.SPLIT_CHARACTER.join([currency, fiat])


class GDAXClientHelper(ClientHelper):
    def __init__(self, **credentials):
        self.client = GDAXClient(**credentials)

        super(GDAXClientHelper, self).__init__()

    def get_currencies(self):
        return self.client.get_info()['funds'].keys()

    def get_ticker(self):
        return self.client.ticker()

    def get_pairs(self):
        pairs = self.client.get_products()

        return [self._from_client_pair(pair) for pair in pairs]

    def _to_client_pair(self, pair):
        [fiat, currency] = self._to_fiat_currency(pair)

        if fiat in self.fiats:
            return pair

        return self.SPLIT_CHARACTER.join([currency, fiat])
