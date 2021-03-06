from bittrex.bittrex import Bittrex as BittrexClient

from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys_values
from crypto_mediator.settings import BITTREX


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
        'last': ('Last', ),
        'highest_bid': ('Bid', ),
        'lowest_ask': ('Ask', ),
        'base_volume': ('BaseVolume', ),
        'current_volume': ('Volume', ),
        'high': ('High', ),
        'low': ('Low', ),
        'updated': ('TimeStamp', ),
    }

    NAME = BITTREX
    CLIENT_CLASS = BittrexClient
    SPLIT_CHARACTER = '-'

    def get_ticker(self):
        ticker_response = self.client.get_market_summaries()

        if not ticker_response['success']:
            raise ClientError(ticker_response['message'])

        return ticker_response

    def get_ticker_parser(self, response, value_types):
        parsed = {}

        for entry in response['result']:
            client_pair = entry.pop('MarketName')
            mediator_pair = self.mediator_pair(client_pair)
            parsed[mediator_pair] = rename_keys_values(
                entry,
                self.TICKER_MAP,
                value_types,
                BITTREX,
                should_be_filled=False
            )

        return parsed

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