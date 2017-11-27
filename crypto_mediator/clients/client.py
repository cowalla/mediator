import time
from dateutil.parser import parse

from crypto_mediator.clients.helpers import (
    BittrexClientHelper, GatecoinClientHelper, GDAXClientHelper, LiquiClientHelper, PoloniexClientHelper
)
from crypto_mediator.settings import BITTREX, GATECOIN, GDAX, LIQUI, POLONIEX, EMPTY


def downcased(string):
    return str(string).lower()


def timestamp(data):
    try:
        return float(data)
    except:
        pass

    parsed = parse(data)

    return time.mktime(parsed.timetuple())


class MetaClient(object):
    """
    Interacts with cryptocurrency market clients to,
     - standardize interactions
     - easily interact with multiple clients
     - trade across multiple exchanges

    expects client credentials in the form,
        exchange: {
          key: ...,
          secret: ...,
    """
    HELPER_MAP = {
        BITTREX: BittrexClientHelper,
        GATECOIN: GatecoinClientHelper,
        GDAX: GDAXClientHelper,
        LIQUI: LiquiClientHelper,
        POLONIEX: PoloniexClientHelper,
    }

    def __init__(self, **exchange_kwargs):
        super(MetaClient, self).__init__()

        self.helpers = {}

        for exchange, kwargs in exchange_kwargs.iteritems():
            HelperClass = self.HELPER_MAP.get(exchange)

            if HelperClass is None:
                raise NotImplementedError('{} is not implemented!'.format(exchange))

            self.helpers[exchange] = HelperClass(**kwargs)

    def request(self, exchange, endpoint, *args, **kwargs):
        helper = self.helpers[exchange]
        helper_function = getattr(helper, endpoint)

        if not helper_function:
            raise NotImplementedError('Helper function "{}" for exchange "{}" not found!'.format(endpoint, exchange))

        return helper_function(*args, **kwargs)

    def get_cached_attribute(self, exchange, attr):
        helper = self.helpers[exchange]
        value = getattr(helper, attr, EMPTY)

        if value is EMPTY:
            raise AttributeError('Attribute not found')

        return value

    def currencies(self, exchange, use_cache=True):
        """
        Given an exchange, returns all currencies on that exchange
        """
        if use_cache:
            response = self.get_cached_attribute(exchange, 'currencies')
        else:
            response = self.request(exchange, 'get_currencies')

        return [
            downcased(currency)
            for currency in response
        ]

    def pairs(self, exchange, use_cache=True):
        """
        Given an exchange, returns all trading pairs
        """
        if use_cache:
            response = self.get_cached_attribute(exchange, 'pairs')
        else:
            response = self.request(exchange, 'get_pairs')

        return [
            downcased(pair)
            for pair in response
        ]

    def _in_ticker_format(self, entry):
        FIELDS = [
            ('average', float),
            ('base_volume', float),
            ('current_volume', float),
            ('high', float),
            ('highest_bid', float),
            ('id', int),
            ('is_frozen', int),
            ('last', float),
            ('low', float),
            ('lowest_ask', float),
            ('percent_change', float),
            ('quote_volume', float),
            ('updated', timestamp),
        ]

        for field, fieldtype in FIELDS:
            value = entry.get(field)

            if value is not None:
                entry[field] = fieldtype(value)

        return entry

    def ticker(self, exchange):
        """
        Given an exchange, returns the ticker for all trading pairs
        """
        response = self.request(exchange, 'get_ticker')

        for pair, ticker in response.iteritems():
            response[pair] = self._in_ticker_format(ticker)

        return response

    def product_ticker(self, exchange, pair):
        try:
            response = self.request(exchange, 'get_product_ticker', pair)

            return self._in_ticker_format(response)
        except NotImplementedError:
            return self.ticker(exchange)[pair]
