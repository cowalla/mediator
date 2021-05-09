import time
import logging
from dateutil.parser import parse

from crypto_mediator.clients.helpers import (
    BittrexClientHelper,
    CoinbaseClientHelper,
    GatecoinClientHelper,
    CoinbaseProClientHelper,
    LiquiClientHelper,
    PoloniexClientHelper
)
from crypto_mediator.settings import (
    BITTREX,
    COINBASE,
    GATECOIN,
    COINBASEPRO,
    LIQUI,
    POLONIEX,
    EMPTY
)

logger = logging.getLogger(__name__)


def downcased(string):
    return str(string).lower()


def timestamp(data):
    try:
        return float(data)
    except:
        pass

    parsed = parse(data)

    return time.mktime(parsed.timetuple())


def to_float(data):
    if data is None:
        return 0
    else:
        return float(data)


def to_int(data):
    if data is None:
        return 0
    else:
        return int(data)


def datafield(data):
    return data


def coerce_fields(d, fieldtypes):
    for field, fieldtype in fieldtypes:
        value = d.get(field, EMPTY)

        if value is not EMPTY:
            d[field] = fieldtype(value)

    return d


class ParsedFieldMissing(Exception):
    pass


class ClientInitFailure(Exception):
    pass


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
        COINBASE: CoinbaseClientHelper,
        GATECOIN: GatecoinClientHelper,
        COINBASEPRO: CoinbaseProClientHelper,
        LIQUI: LiquiClientHelper,
        POLONIEX: PoloniexClientHelper,
    }

    def __init__(self, **exchange_kwargs):
        super(MetaClient, self).__init__()

        self.helpers = {}

        for exchange, kwargs in exchange_kwargs.items():
            HelperClass = self.HELPER_MAP.get(exchange)

            if HelperClass is None:
                raise NotImplementedError('{} is not implemented!'.format(exchange))

            try:
                self.helpers[exchange] = HelperClass(**kwargs)
            except BaseException as e:
                logger.error(
                    'Could not create HelperClass for exchange %s, kwargs %s' % (exchange, str(kwargs))
                )
                raise ClientInitFailure from e

    def request(self, exchange, endpoint, has_data_format=False, *args, **kwargs):
        helper = self.helpers[exchange]
        request_function = getattr(helper, endpoint)

        if not request_function:
            raise NotImplementedError('Helper function "{}" for exchange "{}" not found!'.format(endpoint, exchange))

        response = request_function(*args, **kwargs)
        parser_function = getattr(helper, '%s_parser' % endpoint)
        parsed_field_types = getattr(self, ('%s_fields' % endpoint).upper(), None)

        if has_data_format and parsed_field_types is None:
            raise ParsedFieldMissing(
                'Parsed field types for "{}" for exchange "{}" not found!'.format(endpoint, exchange)
            )

        return parser_function(response, parsed_field_types)

    def get_cached_attribute(self, exchange, attr):
        helper = self.helpers[exchange]
        value = getattr(helper, attr, EMPTY)

        if value is EMPTY:
            raise AttributeError('Attribute not found')

        return value

    # formatters

    GET_TICKER_FIELDS = {
        'average': to_float,
        'base_volume': to_float,
        'current_volume': to_float,
        'high': to_float,
        'highest_bid': to_float,
        'id': to_int,
        'is_frozen': to_int,
        'last': to_float,
        'low': to_float,
        'lowest_ask': to_float,
        'percent_change': to_float,
        'price': to_float,
        'quote_volume': to_float,
        'updated': timestamp,
    }
    GET_PRODUCT_TICKER_FIELDS = GET_TICKER_FIELDS

    GET_TRANSFERS_FIELDS = {
        'amount': to_float,
        'currency': str,
        'created': timestamp,
        'description': str,
        'details': datafield,
        'fee': to_float,
        'from': str,
        'exchange': str,
        'txhash': str,
        'to': str,
        'type': str,
    }

    # API methods

    #    Public API methods

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

    def ticker(self, exchange):
        """
        Given an exchange, returns the ticker for all trading pairs
        """
        return self.request(exchange, 'get_ticker', has_data_format=True)

    def product_ticker(self, exchange, pair):
        try:
            return self.request(exchange=exchange, endpoint='get_product_ticker', has_data_format=True, pair=pair)
        except NotImplementedError:
            return self.ticker(exchange)[pair]

    #    Authenticated methods

    #       Trading methods

    def create_buy_limit_order(self, exchange, pair, amount, price, **kwargs):
        return self.request(exchange, 'create_buy_limit_order', pair, amount, price, **kwargs)

    def create_sell_limit_order(self, exchange, pair, amount, price, **kwargs):
        return self.request(exchange, 'create_sell_limit_order', pair, amount, price, **kwargs)

    #       Account methods

    def transfers(self, exchange, currency=None):
        """
        amount
        created
        currency
        txhash
        exchange
        """
        return sorted(
            self.request(exchange, 'get_transfers', True, currency),
            key=lambda x: x['created']
        )



