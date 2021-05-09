# fiat ticker names
BITCOIN = 'btc'
ETHEREUM = 'eth'
USD = 'usd'
USDT = 'usdt'
LTC = 'ltc'
DASH = 'dash'
ZCASH = 'zec'

FIATS = [
    USD,
    USDT,
    BITCOIN,
    ETHEREUM,
    LTC,
    DASH,
    ZCASH,
]

# character that splits currency pairs. "fiat<split>currency"
MEDIATOR_SPLIT_CHARACTER = '_'

# supported exchanges
BITTREX = 'bittrex'
COINBASE = 'coinbase'
GATECOIN = 'gatecoin'
COINBASEPRO = 'coinbasepro'
LIQUI = 'liqui'
POLONIEX = 'poloniex'

# used for unset values
class EmptyClass(object):
    def __repr__(self):
        return '<EMPTY>'

EMPTY = EmptyClass()
