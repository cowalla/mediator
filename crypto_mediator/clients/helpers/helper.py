from crypto_mediator.settings import FIATS, MEDIATOR_SPLIT_CHARACTER, EMPTY


class ClientError(AttributeError):
    pass


def delete_if_exists(d, key):
    if d.get(key, EMPTY) is not EMPTY:
        del d[key]


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


def rename_keys(data, map):
    return {
        local_key: data[client_key]
        for client_key, local_key in map.iteritems()
        if data.get(client_key) is not None
    }


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

    def get_currencies(self):
        raise NotImplementedError

    def trade_history(self):
        raise NotImplementedError

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self.mediator_pair(pair) for pair in pairs]

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

