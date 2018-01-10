from crypto_mediator.clients.client import MetaClient
from crypto_mediator.secret import (
    BITTREX_API_KEY, BITTREX_API_SECRET,
    GATECOIN_API_KEY, GATECOIN_API_SECRET,
    GDAX_API_KEY, GDAX_API_SECRET, GDAX_PASSPHRASE,
    LIQUI_API_KEY, LIQUI_API_SECRET,
    POLONIEX_API_KEY, POLONIEX_API_SECRET,
)


kwargs = {
    'liqui': {'key': LIQUI_API_KEY, 'secret': LIQUI_API_SECRET},
    'poloniex': {'key': POLONIEX_API_KEY, 'secret': POLONIEX_API_SECRET},
    'bittrex': {'api_key': BITTREX_API_KEY, 'api_secret': BITTREX_API_SECRET},
    'gdax': {'key': GDAX_API_KEY, 'b64secret': GDAX_API_SECRET, 'passphrase': GDAX_PASSPHRASE},
    'gatecoin': {'key': GATECOIN_API_KEY, 'secret': GATECOIN_API_SECRET},
}
client = MetaClient(**kwargs)


if __name__ == '__main__':
    import pdb
    pdb.set_trace()
