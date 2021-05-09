from poloniex import Poloniex as PoloniexClient

from crypto_mediator.clients.helpers.helper import ClientHelper, rename_keys_values
from crypto_mediator.settings import POLONIEX


class PoloniexClientHelper(ClientHelper):
    TICKER_MAP = {
        'id': ('id', ),
        'last': ('last', ),
        'lowest_ask': ('lowestAsk', ),
        'highest_bid': ('highestBid', ),
        'percent_change': ('percentChange', ),
        'base_volume': ('baseVolume', ),
        'quote_volume': ('quoteVolume', ),
        'is_frozen': ('isFrozen', ),
        'high': ('high24hr', ),
        'low': ('low24hr', ),
    }

    NAME = POLONIEX
    CLIENT_CLASS = PoloniexClient

    def get_currencies(self):
        return self.client.returnCurrencies().keys()

    def get_ticker(self):
        return self.client.returnTicker()

    def get_ticker_parser(self, response, value_types):
        parsed = {}

        for pair, data in response.items():
            mediator_pair = self.mediator_pair(pair)
            values = rename_keys_values(data, self.TICKER_MAP, value_types)
            parsed[mediator_pair] = values

        return parsed

    def _get_client_pairs(self):
        return self.get_ticker().keys()
