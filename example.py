from clients.client import MetaClient


kwargs = {'liqui': {}, 'poloniex': {}, 'bittrex': {'api_key': None, 'api_secret': None}}
client = MetaClient(**kwargs)


if __name__ == '__main__':
    # liqui_ticker = client.ticker('liqui')
    # poloniex_ticker = client.ticker('poloniex')
    #
    # liqui_pairs = client.pairs('liqui')
    # poloniex_pairs = client.pairs('poloniex')

    bittrex_ticker = client.ticker('bittrex')

    import pdb
    pdb.set_trace()