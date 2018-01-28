from crypto_mediator.clients.gatecoin import GatecoinClient
from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys, sorted_by_fiat
from crypto_mediator.settings import GATECOIN, MEDIATOR_SPLIT_CHARACTER


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
            raise ClientError('No response from Gatecoin.')

        ticker = {}

        for currency_ticker in response:
            client_pair = currency_ticker['currencyPair']
            mediator_pair = self.mediator_pair(client_pair)
            ticker[mediator_pair] = rename_keys(currency_ticker, self.TICKER_MAP)

        return ticker