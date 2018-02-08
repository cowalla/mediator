from liqui import Liqui as LiquiClient

from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys_values
from crypto_mediator.settings import LIQUI


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

        return ticker_response

    def get_ticker_parser(self, response, value_types):
        parsed = {}

        for pair, data in response.iteritems():
            mediator_pair = self.mediator_pair(pair)
            parsed_ticker_value = rename_keys_values(data, self.TICKER_MAP, value_types)
            parsed[mediator_pair] = parsed_ticker_value

        return parsed


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
