"""
Establishes fiat types and precedence in currency pairs
"""

# ticker names
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


class InvalidCurrencyPairError(SyntaxError):
    pass


class Pair(object):
    FIATS = FIATS

    def __init__(self, *currencies):
        if len(currencies) != 2:
            raise InvalidCurrencyPairError('{} is not a valid pair'.format(str(currencies)))

        [self.fiat, self.currency] = [c for _, c in sorted(zip(self.FIATS, currencies))]

    def to_string(self):
        return '{}_{}'.format(self.fiat, self.currency)


def get_pair(currency_pair):
    currencies = currency_pair.lower().split('_')

    return '_'.join([c for _, c in sorted(zip(FIATS, currencies))])
