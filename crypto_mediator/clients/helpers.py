import json
import requests
from dateutil import parser

from bittrex.bittrex import Bittrex as BittrexClient
from coinbase.wallet.client import Client as CoinbaseClient
from gdax import AuthenticatedClient as GDAXAuthenticatedClient, PublicClient as GDAXPublicClient
from liqui import Liqui as LiquiClient
from poloniex import Poloniex as PoloniexClient

from crypto_mediator.settings import(
    FIATS, MEDIATOR_SPLIT_CHARACTER, BITTREX, COINBASE, GATECOIN, GDAX, LIQUI, POLONIEX, EMPTY
)
from crypto_mediator.clients.gatecoin import GatecoinClient


class ClientError(AttributeError):
    pass


def percent_difference(a, b):
    return 100.0 * (abs(abs(a) - abs(b)) / abs(a))


def to_datetime(str):
    return parser.parse(str)


def delete_if_exists(d, key):
    if d.get(key, EMPTY) is not EMPTY:
        del d[key]


def timestamps_are_within_one_minute(ts1, ts2):
    return abs((to_datetime(ts1) - to_datetime(ts2)).total_seconds()) < 60


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

        # cache for queried constants
        self.cache = {}

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
        self.set_account_info()

    def _from_cache(self, key):
        return self.cache[key]

    def get_currencies(self):
        raise NotImplementedError

    def trade_history(self):
        raise NotImplementedError

    def get_pairs(self):
        pairs = self._get_client_pairs()

        return [self.mediator_pair(pair) for pair in pairs]

    def get_accounts(self):
        pass

    def get_transactions(self, currency):
        raise NotImplementedError

    def set_account_info(self):
        self.accounts = {}
        self.addresses = {}
        self.currency_account_id_map = {}

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

    def mediator_transaction(self, transaction):
        pass

    def mediator_pair(self, pair):
        fiat_currency = pair.split(self.SPLIT_CHARACTER)

        return MEDIATOR_SPLIT_CHARACTER.join(sorted_by_fiat(fiat_currency))


class BittrexClientHelper(ClientHelper):
    """
    client ticker keys:
        [
            'PrevDay': ,'PrevDay'
            'Volume': ,'Volume'
            'Last': ,'Last'
            'OpenSellOrders': ,'OpenSellOrders'
            'TimeStamp': ,'TimeStamp'
            'Bid': ,'Bid'
            'Created': ,'Created'
            'OpenBuyOrders': ,'OpenBuyOrders'
            'High': ,'High'
            'MarketName': ,'MarketName'
            'Low': ,'Low'
            'Ask': ,'Ask'
            'BaseVolume': ,'BaseVolume'
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

    def _get_client_pairs(self):
        markets_response = self.client.get_markets()

        return [
            self.SPLIT_CHARACTER.join([r['BaseCurrency'], r['MarketCurrency']])
            for r in markets_response['result']
        ]

class CoinbaseClientHelper(ClientHelper):

    NAME = COINBASE
    CLIENT_CLASS = CoinbaseClient
    SPLIT_CHARACTER = '-'

    def __init__(self, *args, **kwargs):
        super(CoinbaseClientHelper, self).__init__(*args, **kwargs)

        self.set_account_info()
        self.currency_account_id_map = {
            currency: self.accounts[currency].id
            for currency in self.currencies
        }

    def get_ticker(self):
        raise NotImplementedError

    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    def _get_client_pairs(self):
        client_currencies = ['BTC', 'ETH', 'LTC', 'BCH']
        fiat = 'USD'

        return [
            self.SPLIT_CHARACTER.join([currency, fiat])
            for currency in client_currencies
        ]

    def _get_account_transactions(self, account_id):
        return self.client.get_transactions(account_id).data

    def mediator_transaction(self, transaction):
        return {
            'amount': float(transaction.amount.amount),
            'created': to_datetime(transaction.created_at),
            'currency': transaction.amount.currency.lower(),
            'txhash': transaction.network['hash'] if transaction.network else None,
            'exchange': self.NAME,
        }

    def get_transactions(self, currency):
        account_id = self.currency_account_id_map[currency]

        return sorted(
            self._get_account_transactions(account_id),
            key=lambda x:x['created_at']
        )

    def get_accounts(self):
        return self.client.get_accounts().data

    def set_account_info(self):
        # set accounts
        self.accounts = {
            account['balance']['currency'].lower(): account
            for account in self.get_accounts()
        }
        # set addresses
        self.addresses = {
            currency: account.get_addresses().data
            for currency, account in self.accounts.iteritems()
        }
        # set id map
        self.currency_account_id_map = {
            currency: self.accounts[currency].id
            for currency in self.currencies
        }

    def _transactions_passthrough_to_gdax(self, transactions):
        # finds transactions pairs that pass through to gdax (received, sent),
        # requires transactions to be sorted by date
        passthroughs = []
        current_passthrough = []
        # look for transfers to gdax first, which have to come after deposits to coinbase
        transactions.reverse()

        for transaction in transactions:
            has_exchange_deposit = len(current_passthrough) == 1
            transaction_type = transaction.type
            amount = float(transaction.amount.amount)

            if not has_exchange_deposit and not transaction_type == 'exchange_deposit':
                continue
            if has_exchange_deposit:
                if not transaction_type == 'send':
                    continue

                # check amounts to make sure this is a matching transaction
                passthrough_amount = float(current_passthrough[0].amount.amount)

                if percent_difference(amount, passthrough_amount) > 1.0:
                    # not a match!
                    continue

            current_passthrough.append(transaction)
            is_complete = len(current_passthrough) == 2

            if is_complete:
                # complete passthrough
                current_passthrough.reverse()
                passthroughs.append(current_passthrough)
                current_passthrough = []

        passthroughs.reverse()

        return passthroughs

    def get_gdax_deposits(self, currency):
        transactions = self.get_transactions(currency)
        passthroughs = self._transactions_passthrough_to_gdax(transactions)

        # returns initial coinbase deposit (that coinbase passes through to gdax)
        return [passthrough[0] for passthrough in passthroughs]


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

    # account info

    def get_accounts(self):
        response = self.client.get_accounts()

        return {account['currency'].lower(): account for account in response}

    def get_transactions(self, currency):
        account_id = self.currency_account_id_map[currency]
        return sorted(
            flatten(self.client.get_account_history(account_id)),
            key=lambda x: x['created_at']
        )

    def get_withdrawals(self):
        pass

    def get_deposits(self):
        pass

    def set_account_info(self):
        # set accounts
        self.accounts = self.get_accounts()
        # set addresses
        self.addresses = {}
        # set id map
        self.currency_account_id_map = {
            currency: self.accounts.get(currency, {}).get('id', None)
            for currency in self.currencies
        }

    # helpers

    def mediator_transaction(self, transaction):
        # {u'created_at': u'2017-10-17T07:26:12.397213Z', u'amount': u'15.9820000000000000',
        #  u'details': {u'transfer_id': u'd2aa7c06-df2b-4b14-a917-db4bb5889169',
        #               u'transfer_type': u'deposit'}, u'balance': u'15.9820000000000000',
        #  u'type': u'transfer', u'id': 314490389}

        return {
            'amount': float(transaction['amount']),
            'created': to_datetime(transaction['created_at']),
            'currency': transaction['amount'],
            'exchange': self.NAME,
        }


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
    TRANSFER_MAP = {
         'From': 'from_address',
         'Symbol': 'currency',
         'Time': 'timestamp',
         'TxKey': 'txkey',
         'TxHash': 'txhash',
         'Amount': 'amount',
         'Confirmations': 'confirmations',
         'Address': 'to_address',
         'Memo': 'memo',
    }
    TRANSFER_URL = 'http://webapi.liqui.io/{TYPE}/History'

    NAME = LIQUI
    CLIENT_CLASS = LiquiClient
    MAX_TRADE_COUNT = 1000

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

    def trade_history(self, **kwargs):
        # most recent trades limited to `MAX_TRADE_COUNT`
        response = self.client.trade_history(**kwargs)
        trades = response.values()

        for trade in trades:
            trade['pair'] = self.mediator_pair(trade['pair'])

        return sorted(trades, key=lambda x: x['trade_id'])

    def get_trade_history(self):
        # gets all trade history
        if not 'first_trade' in self.cache:
            first = self.trade_history(count=1)
            self.cache['first_trade'] = first[0] if first else []

        first_trade_id = self._from_cache('first_trade')['trade_id']
        new_trades = self.trade_history(from_id=first_trade_id)
        trades = []

        while len(new_trades) > 0:
            trades += new_trades

            if len(new_trades) < self.MAX_TRADE_COUNT:
                # gotten to end of trades
                break

            first_trade_id = trades[-1]['trade_id']
            new_trades = self.trade_history(from_id=first_trade_id)[1:]

        return trades

    def get_deposits(self, key):
        return self.get_transfers(key, 'Deposit')

    def get_withdrawals(self, key):
        return self.get_transfers(key, 'Withdraw')

    def get_transfers(self, key, transfer_type=None):
        # Need to use the web api which requires a session key.
        # Visit /Balances and looking in the network requests for the payload.
        if transfer_type not in ('Withdraw', 'Deposit'):
            raise ClientError('Use "Withdraw" or "Deposit"')

        url = self.TRANSFER_URL.format(TYPE=transfer_type)
        params = {'Id': 0, 'key': key}
        response = requests.post(url, params)

        return [
            rename_keys(json.loads(transaction['Data']), self.TRANSFER_MAP)
            for transaction in response.json()['Value']
        ]

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
