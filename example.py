from clients.client import MetaClient


kwargs = {'liqui': {}, 'poloniex': {}}
client = MetaClient(**kwargs)


if __name__ == '__main__':
    liqui_ticker = client.ticker('liqui')
    poloniex_ticker = client.ticker('poloniex')

    liqui_pairs = client.pairs('liqui')
    poloniex_pairs = client.pairs('poloniex')

    import pdb
    pdb.set_trace()