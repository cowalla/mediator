from bittrex.bittrex import Bittrex as BittrexClient
from gdax import AuthenticatedClient as GDAXAuthenticatedClient, PublicClient as GDAXPublicClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from crypto_mediator.settings import FIATS, MEDIATOR_SPLIT_CHARACTER, BITTREX, GATECOIN, GDAX, LIQUI, POLONIEX, EMPTY
from crypto_mediator.clients.gatecoin import GatecoinClient


class ClientError(AttributeError):
    pass


def delete_if_exists(d, key):
    if d.get(key, EMPTY) is not EMPTY:
        del d[key]


def flatten(l):
    # flattens a list one level
    flattened = []

    for item in l:
        if isinstance(item, list):
            flattened += item
        elif isinstance(item, tuple):
            flattened += list(item)
        else:
            flattened.append(item)

    return flattened


def get_fiat_order(f, fiat_order):
    try:
        return fiat_order.index(f)
    except ValueError:
        # not in fiat_order
        return None


def rename_keys(data, map):
    return {
        local_key: data[client_key]
        for client_key, local_key in map.iteritems()
        if data.get(client_key) is not None
    }


def sorted_by_fiat(currencies, fiat_order=None):
    if fiat_order is None:
        # Mediator order
        fiat_order = FIATS
    if len(currencies) != 2:
        # this function could be opened up to sort any length, if necessary
        raise NotImplementedError

    [a, b] = currencies
    a = a.lower()
    b = b.lower()
    a_index, b_index = get_fiat_order(a, fiat_order), get_fiat_order(b, fiat_order)

    if b_index is None:
        return a, b
    elif a_index is None:
        return b, a
    elif a_index < b_index:
        return a, b
    else:
        return b, a


def sort_pair_by_fiat(currency_pair, split_character=None, fiat_order=None):
    """
    Orders a currency pair according to the order provided.

    Exchanges do not agree which currency should come first in a pair, e.g. usdt-btc or btc-usdt.
    Returns a pair (or any array) sorted according to fiat_order.
    """
    if split_character is None:
        split_character = MEDIATOR_SPLIT_CHARACTER

    currencies = currency_pair.split(split_character)
    sorted_pair = sorted_by_fiat(currencies, fiat_order)

    return MEDIATOR_SPLIT_CHARACTER.join(sorted_pair)

class ClientHelper(object):
    NAME = None
    CLIENT_CLASS = None
    SPLIT_CHARACTER = '_'

    def __init__(self, *args, **kwargs):
        super(ClientHelper, self).__init__()

        self.fiats = set()
        self.pairs = []
        self.currencies = []
        self.client = self.CLIENT_CLASS(*args, **kwargs)

        self.client_pairs = sorted(self._get_client_pairs())
        self.pair_map = {
            self.mediator_pair(p): p
            for p in self.client_pairs
        }
        self.pairs = sorted(self.pair_map.keys())
        self.fiats = self._get_fiats_from_mediator_pairs(self.pairs)
        self.currencies = self.get_currencies()

    def get_currencies(self):
        raise NotImplementedError

    def trade_history(self):
        raise NotImplementedError

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self.mediator_pair(pair) for pair in pairs]

    def _get_client_pairs(self):
        raise NotImplementedError

    def _to_client_pair(self, pair):
        # translates a pair from `Mediator` format to its own client format
        return self.pair_map[pair]

    def _get_fiats_from_mediator_pairs(self, pairs):
        fiats = set([pair.split(MEDIATOR_SPLIT_CHARACTER)[0] for pair in pairs])

        return list(fiats)

    def _get_currencies_from_mediator_pairs(self, pairs):
        flat = flatten([pair.split(MEDIATOR_SPLIT_CHARACTER) for pair in pairs])

        return list(set(flat))

    def mediator_pair(self, pair):
        fiat_currency = pair.split(self.SPLIT_CHARACTER)

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))


class BittrexClientHelper(ClientHelper):
    """
    client ticker keys:
        [
            u'PrevDay',
            u'Volume',
            u'Last',
            u'OpenSellOrders',
            u'TimeStamp',
            u'Bid',
            u'Created',
            u'OpenBuyOrders',
            u'High',
            u'MarketName',
            u'Low',
            u'Ask',
            u'BaseVolume',
        ]
    """
    TICKER_MAP = {
        'Last': 'last',
        'Bid': 'highest_bid',
        'Ask': 'lowest_ask',
        'BaseVolume': 'base_volume',
        'Volume': 'current_volume',
        'High': 'high',
        'Low': 'low',
        'TimeStamp': 'updated',
    }

    NAME = BITTREX
    CLIENT_CLASS = BittrexClient
    SPLIT_CHARACTER = '-'

    def get_ticker(self):
        ticker_response = self.client.get_market_summaries()

        if not ticker_response['success']:
            raise ClientError(ticker_response['message'])

        ticker = {}

        for entry in ticker_response['result']:
            client_pair = entry.pop('MarketName')
            mediator_pair = self.mediator_pair(client_pair)

            ticker[mediator_pair] = rename_keys(entry, self.TICKER_MAP)

        return ticker

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    def get_pairs(self):
        client_pairs = self._get_client_pairs()

        return [
            self.mediator_pair(pair)
            for pair in client_pairs
        ]

    def _get_client_pairs(self):
        markets_response = self.client.get_markets()

        return [
            self.SPLIT_CHARACTER.join([r['BaseCurrency'], r['MarketCurrency']])
            for r in markets_response['result']
        ]

class GatecoinClientHelper(ClientHelper):
    NAME = GATECOIN
    CLIENT_CLASS = GatecoinClient
    SPLIT_CHARACTER = ''

    TICKER_MAP = {
        'last': 'last',
        'bid': 'highest_bid',
        'ask': 'lowest_ask',
        'volume': 'base_volume',
        'high': 'high',
        'low': 'low',
        'createDateTime': 'updated',
        'vwap': 'average',
    }

    def mediator_pair(self, pair):
        # I hate you gatecoin
        fiat = pair[:len(pair)/2]
        currency = pair[len(pair)/2:]
        fiat_currency = [fiat, currency]

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))

    def _get_client_pairs(self):
        return [t['currencyPair'] for t in self.client.livetickers().get('tickers')]

    def get_currencies(self, use_cache=True):
        self.pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(self.pairs)

    def get_ticker(self):
        response = self.client.livetickers().get('tickers')

        if not response:
            print response
            raise ClientError('No response from Gatecoin.')

        ticker = {}

        for currency_ticker in response:
            client_pair = currency_ticker['currencyPair']
            mediator_pair = self.mediator_pair(client_pair)
            ticker[mediator_pair] = rename_keys(currency_ticker, self.TICKER_MAP)

        return ticker


class GDAXClientHelper(ClientHelper):
    # unlikely to be used in the future
    NAME = GDAX
    CLIENT_CLASS = GDAXAuthenticatedClient
    TICKER_MAP = {
        'bid': 'highest_bid',
        'ask': 'lowest_ask',
        'volume': 'current_volume',
        'time': 'updated',
        'price': 'price',
    }
    # ACTIVE_ORDER_MAP = {
    #     'status',
    #     'created_at',
    #     'post_only',
    #     'product_id',
    #     'fill_fees',
    #     'settled',
    #     'price',
    #     'executed_value',
    #     'id',
    #     'time_in_force',
    #     'stp',
    #     'filled_size',
    #     'type',
    #     'side',
    #     'size',
    # }
    SPLIT_CHARACTER = '-'

    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
           self.CLIENT_CLASS = GDAXPublicClient

        super(GDAXClientHelper, self).__init__(*args, **kwargs)

    def get_currencies(self):
        return [p['id'].lower() for p in self.client.get_currencies()]

    def get_ticker(self):
        raise NotImplementedError('API does not allow polling for all pairs')

    def get_product_ticker(self, pair):
        client_pair = self.pair_map[pair]
        response = self.client.get_product_ticker(client_pair)

        return rename_keys(response, self.TICKER_MAP)

    def _get_client_pairs(self):
        return [p['id'] for p in self.client.get_products()]

    def create_buy_limit_order(self, pair, amount, price):
        return self.create_order(side='buy', type='limit', pair=pair, size=amount, price=price)

    def create_buy_market_order(self, pair, amount):
        return self.create_order(side='buy', type='market', pair=pair, size=amount)

    def create_buy_stop_order(self, pair, amount):
        return self.create_order(side='buy', type='stop', pair=pair, size=amount)

    def create_sell_limit_order(self, pair, amount, price):
        return self.create_order(side='sell', type='limit', pair=pair, size=amount, price=price)

    def create_sell_market_order(self, pair, amount):
        return self.create_order(side='sell', type='market', pair=pair, funds=amount)

    def create_sell_stop_order(self, pair, amount):
        return self.create_order(side='sell', type='stop', pair=pair, funds=amount)

    def create_order(self, **kwargs):
        '''
        client_oid	[optional] Order ID selected by you to identify your order
        type	[optional] limit, market, or stop (default is limit)
        side	buy or sell
        product_id	A valid product id
        stp	[optional] Self-trade prevention flag

        LIMIT ORDER PARAMETERS
        Param	Description
        price	Price per bitcoin
        size	Amount of BTC to buy or sell
        time_in_force	[optional] GTC, GTT, IOC, or FOK (default is GTC)
        cancel_after	[optional]* min, hour, day
        post_only	[optional]** Post only flag
        * Requires time_in_force to be GTT

        ** Invalid when time_in_force is IOC or FOK

        MARKET ORDER PARAMETERS
        size	[optional]* Desired amount in BTC (fiat?)
        funds	[optional]* Desired amount of quote currency to use
        * One of size or funds is required.

        STOP ORDER PARAMETERS
        price	Desired price at which the stop order triggers
        size	[optional]* Desired amount in BTC
        funds	[optional]* Desired amount of quote currency to use
        * One of size or funds is required.

        MARGIN PARAMETERS
        overdraft_enabled	* If true funding will be provided if the order's cost cannot be covered by the account's balance
        funding_amount	* Amount of funding to be provided for the order
        '''
        pair = kwargs.pop('pair')
        kwargs['product_id'] = self.pair_map[pair]

        if kwargs['side'] == 'buy':
            return self.client.buy(**kwargs)
        if kwargs['side'] == 'sell':
            return self.client.sell(**kwargs)

        raise ClientError('Invalid side %s' % kwargs['side'])


class LiquiClientHelper(ClientHelper):
    TICKER_MAP = {
        'last': 'last',
        'buy': 'highest_bid',
        'sell': 'lowest_ask',
        'vol': 'base_volume',
        'vol_cur': 'current_volume',
        'high': 'high',
        'low': 'low',
        'updated': 'updated',
        'avg': 'average',
    }

    NAME = LIQUI
    CLIENT_CLASS = LiquiClient

    # public methods

    def get_ticker(self):
        all_liqui_pairs = [self._to_client_pair(p) for p in self.pairs]
        pair = '-'.join(all_liqui_pairs)
        ticker_response = self.client.ticker(pair=pair)

        if ticker_response.get('error'):
            raise ClientError(ticker_response['error'])

        return {
            self.mediator_pair(pair): rename_keys(data, self.TICKER_MAP)
            for pair, data in ticker_response.iteritems()
        }

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    # account information

    def trade_history(self):
        response = self.client.trade_history()
        trades = response.values()

        for trade in trades:
            trade['pair'] = self.mediator_pair(trade['pair'])

        return sorted(trades, key=lambda x: x['timestamp'])

    def _get_client_pairs(self):
        return self.client.info()['pairs'].keys()


class PoloniexClientHelper(ClientHelper):
    TICKER_MAP = {
        'id': 'id',
        'last': 'last',
        'lowestAsk': 'lowest_ask',
        'highestBid': 'highest_bid',
        'percentChange': 'percent_change',
        'baseVolume': 'base_volume',
        'quoteVolume': 'quote_volume',
        'isFrozen': 'is_frozen',
        'high24hr': 'high',
        'low24hr': 'low',
    }

    NAME = POLONIEX
    CLIENT_CLASS = PoloniexClient

    def get_currencies(self):
        return self.client.returnCurrencies().keys()

    def get_ticker(self):
        ticker_response = self.client.returnTicker()

        return {
            self.mediator_pair(pair): rename_keys(data, self.TICKER_MAP)
            for pair, data in ticker_response.iteritems()
        }

    def _get_client_pairs(self):
        return self.get_ticker().keys()
