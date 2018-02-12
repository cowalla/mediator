import time
from collections import defaultdict
from dateutil.parser import parse

from crypto_mediator.settings import FIATS, MEDIATOR_SPLIT_CHARACTER, EMPTY


class ClientError(AttributeError):
    pass


def delete_if_exists(d, key):
    if d.get(key, EMPTY) is not EMPTY:
        del d[key]


def percent_difference(a, b):
    return 100.0 * (abs(abs(a) - abs(b)) / abs(a))


def to_datetime(str):
    return parse(str)


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


def get_fiat_order(f, fiat_order):
    try:
        return fiat_order.index(f)
    except ValueError:
        # not in fiat_order
        return None


class GetValueError(BaseException):
    pass


def get_value(data, *keys):
    if len(keys) == 0 or data is EMPTY:
        return data

    key = keys[0]

    try:
        value = data.get(key, EMPTY)
    except AttributeError:
        raise GetValueError('Data "%s" cannot be gotten from' % str(data))

    if len(keys) == 0:
        return value

    return get_value(value, *keys[1:])


def rename_keys_values(data, key_map, value_types, exchange_name=None, should_be_filled=True):
    """
    Takes data from a response and,
       Renames the keys according to key_map
       Coherces the values according to value_types
    """
    renamed_keys_and_values = {}

    for client_key, key_path in key_map.iteritems():
        value = get_value(data, *key_path)

        if should_be_filled and value is EMPTY:
            message = 'Empty value found in response when it should be present. \nkey:"{}"\ndata:"{}"'.format(
                client_key,
                data
            )

            raise ClientError(message)

        try:
            coherce_value_function = value_types[client_key]
        except KeyError:
            raise ClientError('No specified data type for client field %s' % client_key)

        if value is not EMPTY:
            # coherce to specified data type
            value = coherce_value_function(value)

        renamed_keys_and_values[client_key] = value

    if exchange_name:
        renamed_keys_and_values['exchange'] = exchange_name

    return renamed_keys_and_values


def group_objects_by(objects, key):
    groups = defaultdict(list)

    for o in objects:
        groups[o[key]].append(o)

    return groups


def sorted_by_fiat(currencies, fiat_order=None):
    if fiat_order is None:
        # Mediator order
        fiat_order = FIATS
    if len(currencies) != 2:
        # this function could be opened up to sort any length, if necessary
        raise NotImplementedError

    [a, b] = currencies
    a = a.lower()
    b = b.lower()
    a_index, b_index = get_fiat_order(a, fiat_order), get_fiat_order(b, fiat_order)

    if b_index is None:
        return a, b
    elif a_index is None:
        return b, a
    elif a_index < b_index:
        return a, b
    else:
        return b, a


def sort_pair_by_fiat(currency_pair, split_character=None, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    if split_character is None:
        split_character = MEDIATOR_SPLIT_CHARACTER

    currencies = currency_pair.split(split_character)
    sorted_pair = sorted_by_fiat(currencies, fiat_order)

    return MEDIATOR_SPLIT_CHARACTER.join(sorted_pair)


def label_indices(data, map):
    return dict(zip(map, data))


def downcased(string):
    return str(string).lower()


def timestamp(data):
    try:
        return float(data)
    except:
        pass

    parsed = parse(data)

    return time.mktime(parsed.timetuple())


def coherce_fields(d, fieldtypes):
    for field, fieldtype in fieldtypes:
        value = d.get(field, EMPTY)

        if value is not EMPTY:
            d[field] = fieldtype(value)

    return d


TICKER_FIELDS = {
        'average': float,
        'base_volume': float,
        'current_volume': float,
        'high': float,
        'highest_bid': float,
        'id': int,
        'is_frozen': int,
        'last': float,
        'low': float,
        'lowest_ask': float,
        'percent_change': float,
        'price': float,
        'quote_volume': float,
        'updated': timestamp,
    }


class ClientHelper(object):
    NAME = None
    CLIENT_CLASS = None
    SPLIT_CHARACTER = '_'

    def __init__(self, *args, **kwargs):
        super(ClientHelper, self).__init__()

        self.fiats = set()
        self.pairs = []
        self.currencies = []
        self.client = self.CLIENT_CLASS(*args, **kwargs)

        self.client_pairs = sorted(self._get_client_pairs())
        self.pair_map = {
            self.mediator_pair(p): p
            for p in self.client_pairs
        }
        self.pairs = sorted(self.pair_map.keys())
        self.fiats = self._get_fiats_from_mediator_pairs(self.pairs)
        self.currencies = self.get_currencies()

    def get_ticker(self, *args, **kwargs):
        raise NotImplementedError

    def get_ticker_parser(self, response, value_types):
        return response

    def get_currencies(self):
        raise NotImplementedError

    def get_currencies_parser(self, response, *args, **kwargs):
        return response

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self.mediator_pair(pair) for pair in pairs]

    def get_pairs_parser(self, response, *args, **kwargs):
        return response

    def trade_history(self):
        raise NotImplementedError

    def trade_history_parser(self, response, *args, **kwargs):
        return response

    def get_transactions(self, *args, **kwargs):
        raise NotImplementedError

    def get_transactions_parser(self, response, values_list):
        return response

    def get_accounts(self, *args, **kwargs):
        raise NotImplementedError

    def _get_client_pairs(self):
        raise NotImplementedError

    def _to_client_pair(self, pair):
        # translates a pair from `Mediator` format to its own client format
        return self.pair_map[pair]

    def _get_fiats_from_mediator_pairs(self, pairs):
        fiats = set([pair.split(MEDIATOR_SPLIT_CHARACTER)[0] for pair in pairs])

        return list(fiats)

    def _get_currencies_from_mediator_pairs(self, pairs):
        flat = flatten([pair.split(MEDIATOR_SPLIT_CHARACTER) for pair in pairs])

        return list(set(flat))

    def mediator_pair(self, pair):
        fiat_currency = pair.split(self.SPLIT_CHARACTER)

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))

    def get_currency(self, pair):
        return pair.split(self.SPLIT_CHARACTER)[1]

    def get_fiat(self, pair):
        return pair.split(self.SPLIT_CHARACTER)[0]

