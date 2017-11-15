"""
Establishes fiat types and precedence in currency pairs
"""

# fiat ticker names
BITCOIN = 'btc'
ETHEREUM = 'eth'
USDT = 'usdt'
LTC = 'ltc'
DASH = 'dash'
ZCASH = 'zec'

FIATS = [
    USDT,
    BITCOIN,
    ETHEREUM,
    LTC,
    DASH,
    ZCASH,
]

SPLIT_CHARACTER = '_'


def sort_pair_by_fiat(currency_pair, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    currencies = currency_pair.lower().split(SPLIT_CHARACTER)

    if fiat_order is None:
        # Mediator order
        fiat_order = FIATS
    if len(currencies) != 2:
        # this function could be opened up to sort any length, if necessary
        raise NotImplementedError

    sorted_by_order = [c for _, c in sorted(zip(fiat_order, currencies))]

    return (sorted_by_order[0], sorted_by_order[1])


# def calculate_precedence(self):
#     # fiat precedence is important to
#     if self.precedence:
#         return self.precedence
#
#     pairs = self.pairs
#     # NOTE: if this fails here then the split character ('_') here is wrong
#     # fiats should be quite small, < 10 elements
#     fiats = set([self.to_fiat_currency(pair)[0] for pair in pairs])
#     fiat_pairings = set()
#
#     for pair in pairs:
#         [fiat, currency] = self.to_fiat_currency(pair)
#
#         if fiat in fiats and currency in fiats:
#             fiat_pairings.add([fiat, currency])
#
#     precedence = defaultdict(lambda: len(fiats))
#
#     for [fiat, currency] in fiat_pairings:
#         precedence[fiat] -=1
#
#     return sorted(precedence, key=lambda (k, v): (v, k)).keys()
