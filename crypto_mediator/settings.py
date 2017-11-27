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
GATECOIN = 'gatecoin'
GDAX = 'gdax'
LIQUI = 'liqui'
POLONIEX = 'poloniex'

# used for unset values
EMPTY = object()