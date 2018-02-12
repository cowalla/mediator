import datetime

from crypto_mediator.clients.client import MetaClient
from crypto_mediator.clients.helpers.helper import group_objects_by
from crypto_mediator.secret import (
    BITTREX_API_KEY, BITTREX_API_SECRET,
    COINBASE_API_KEY, COINBASE_API_SECRET,
    GATECOIN_API_KEY, GATECOIN_API_SECRET,
    GDAX_API_KEY, GDAX_API_SECRET, GDAX_PASSPHRASE,
    LIQUI_API_KEY, LIQUI_API_SECRET,
    POLONIEX_API_KEY, POLONIEX_API_SECRET,
)


def readable_ts(trade):
    return datetime.datetime.fromtimestamp(trade['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

kwargs = {
    # 'liqui': {'key': LIQUI_API_KEY, 'secret': LIQUI_API_SECRET},
    # 'poloniex': {'key': POLONIEX_API_KEY, 'secret': POLONIEX_API_SECRET},
    # 'bittrex': {'api_key': BITTREX_API_KEY, 'api_secret': BITTREX_API_SECRET},
    'coinbase': {'api_key': COINBASE_API_KEY, 'api_secret': COINBASE_API_SECRET},
    'gdax': {'key': GDAX_API_KEY, 'b64secret': GDAX_API_SECRET, 'passphrase': GDAX_PASSPHRASE},
    # 'gatecoin': {'key': GATECOIN_API_KEY, 'secret': GATECOIN_API_SECRET},
}
client = MetaClient(**kwargs)
# gdax_helper = client.helpers['gdax']
# coinbase_accounts = gdax_helper.client.get_coinbase_accounts()
# coinbase_account_id = coinbase_accounts[2]['id']
# coinbase_account_info = gdax_helper.client.get_coinbase_account(coinbase_account_id)

if __name__ == '__main__':
    cb_trans = client.transactions('coinbase', 'ltc')
    trans = client.transactions('gdax', 'ltc')
    import pdb
    pdb.set_trace()