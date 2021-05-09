import copy
import datetime

from crypto_mediator.clients.client import MetaClient

# Define secrets here.
BITTREX_API_KEY = None
BITTREX_API_SECRET = None

COINBASE_API_KEY = None
COINBASE_API_SECRET = None

COINBASEPRO_API_KEY = None
COINBASEPRO_API_SECRET = None
COINBASEPRO_PASSPHRASE = None

POLONIEX_API_KEY = None
POLONIEX_API_SECRET = None


def readable_ts(trade):
    # Take a timestamp and make it human-readable.
    return datetime.datetime.fromtimestamp(trade['timestamp']).strftime('%Y-%m-%d %H:%M:%S')


def gather_kwargs():
    kwargs = {
        'poloniex': {'key': POLONIEX_API_KEY, 'secret': POLONIEX_API_SECRET},
        'bittrex': {'api_key': BITTREX_API_KEY, 'api_secret': BITTREX_API_SECRET},
        'coinbase': {'api_key': COINBASE_API_KEY, 'api_secret': COINBASE_API_SECRET},
        'coinbasepro': {'key': COINBASEPRO_API_KEY, 'b64secret': COINBASEPRO_API_SECRET, 'passphrase': COINBASEPRO_PASSPHRASE},
    }
    mutated = copy.deepcopy(kwargs)
    requires_kwargs = ['coinbase', 'coinbasepro']

    for exchange in kwargs.keys():
        if exchange in requires_kwargs and not all(kwargs[exchange].values()):
            mutated.pop(exchange)

    return mutated


client = MetaClient(**gather_kwargs())
poloniex_ticker = client.ticker('poloniex')
bittrex_ticker = client.ticker('bittrex')
current_ticker = client.product_ticker('coinbasepro', 'usd_btc')
historical_prices = client.helpers['coinbasepro'].get_rates('usd_btc', 60 * 60 * 24)

print('Product ticker for USD-BTC on Coinbase Pro: %s' % current_ticker)
print('Historical prices for USD-BTC on Coinbase Pro for the last 300 days: %s' % historical_prices)

