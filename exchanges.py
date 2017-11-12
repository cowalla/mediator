from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from fiat import get_pair, Pair


class LiquiPair(Pair):
    pass


class LiquiClientHelper(object):
    def __init__(self, **credentials):
        super(LiquiClientHelper, self).__init__()

        self.client = LiquiClient(**credentials)
        self.precedence = []

    def initialize(self):
        pass


    def get_ticker(self, currency_pairs):
        liqui_pairs = [LiquiPair() for p in currency_pairs]

        return self.client.ticker(pair=currency_pairs)

    def get_pairs(self):
        return [Pair(*ps) for ps in self._liqui_pairs()]

    def _liqui_pairs(self):
        return self.client.info()['pairs'].keys()