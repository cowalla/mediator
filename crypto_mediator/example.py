from crypto_mediator.clients.client import MetaClient


kwargs = {
    'liqui': {},
    'poloniex': {},
    'bittrex': {'api_key': None, 'api_secret': None},
    'gdax': {},
    'gatecoin': {},
}
client = MetaClient(**kwargs)


if __name__ == '__main__':
    liqui_ticker = client.ticker('liqui')
    poloniex_ticker = client.ticker('poloniex')
    bittrex_ticker = client.ticker('bittrex')
    gatecoin_ticker = client.ticker('gatecoin')

    import pdb
    pdb.set_trace()