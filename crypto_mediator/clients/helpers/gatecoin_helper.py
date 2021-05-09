# Deprecated. GateCoin doesn't exist anymore.

from crypto_mediator.clients.gatecoin import GatecoinClient
from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys_values, sorted_by_fiat
from crypto_mediator.settings import GATECOIN, MEDIATOR_SPLIT_CHARACTER


class GatecoinClientHelper(ClientHelper):
    NAME = GATECOIN
    CLIENT_CLASS = GatecoinClient
    SPLIT_CHARACTER = ''

    TICKER_MAP = {
        'last': ('last', ),
        'highest_bid': ('bid', ),
        'lowest_ask': ('ask', ),
        'base_volume': ('volume', ),
        'high': ('high', ),
        'low': ('low', ),
        'updated': ('createDateTime', ),
        'average': ('vwap', ),
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

        return response

    def get_ticker_parser(self, response, value_types):
        parsed = {}

        for currency_ticker in response:
            client_pair = currency_ticker['currencyPair']
            mediator_pair = self.mediator_pair(client_pair)
            parsed[mediator_pair] = rename_keys_values(currency_ticker, self.TICKER_MAP, value_types, GATECOIN, False)

        return parsed
