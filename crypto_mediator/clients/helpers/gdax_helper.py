from gdax import AuthenticatedClient as GDAXAuthenticatedClient, PublicClient as GDAXPublicClient

from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys_values, label_indices, flatten
from crypto_mediator.settings import GDAX


class GDAXClientHelper(ClientHelper):
    # unlikely to be used in the future
    NAME = GDAX
    CLIENT_CLASS = GDAXAuthenticatedClient
    SPLIT_CHARACTER = '-'

    TICKER_MAP = {
        'highest_bid': ('bid', ),
        'lowest_ask': ('ask', ),
        'current_volume': ('volume', ),
        'updated': ('time', ),
        'price': ('price', ),
    }
    RATES_INDICES = [
        'timestamp',
        'low',
        'high',
        'open',
        'close',
        'volume',
    ]
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
    TRANSACTIONS_MAP = {
        'amount': ('amount', ),
        'currency': ('currency',),
        'created': ('created_at',),
        'details': ('details',),
    }

    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
           self.CLIENT_CLASS = GDAXPublicClient

        super(GDAXClientHelper, self).__init__(*args, **kwargs)

        self.set_account_info()

    def get_currencies(self):
        return [p['id'].lower() for p in self.client.get_currencies()]

    def get_ticker(self):
        raise NotImplementedError('API does not allow polling for all pairs')

    def get_product_ticker(self, pair):
        client_pair = self.pair_map[pair]

        return self.client.get_product_ticker(client_pair)

    def get_product_ticker_parser(self, response, value_types):
        return rename_keys_values(response, self.TICKER_MAP, value_types, 'gdax', should_be_filled=False)

    def get_rates(self, pair, dt=None, **kwargs):
        if dt is None:
            dt = 60

        kwargs['granularity'] = dt
        client_pair = self.pair_map[pair]
        response = self.client.get_product_historic_rates(product_id=client_pair, **kwargs)
        print str(response)[:200]

        return sorted(
            [label_indices(rate, self.RATES_INDICES) for rate in response],
            key=lambda x: x['timestamp']
        )

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

    def get_accounts(self):
        return self.client.get_accounts()

    def set_account_info(self):
        # set accounts
        self.accounts = {
            account['currency'].lower(): account
            for account in self.get_accounts()
        }
        # set id map
        self.currency_account_id_map = {
            currency: account['id']
            for currency, account in self.accounts.iteritems()
        }

    def _get_transactions(self, currency):
        account_id = self.currency_account_id_map[currency]
        response = self.client.get_account_history(account_id)

        return flatten(response)

    def get_transactions(self, currency, is_transfer):
        transactions = self._get_transactions(currency)

        if is_transfer:
            return (
                currency,
                [
                    t for t in transactions
                    if t['type'] == 'transfer'
                ],
            )

        return (
            currency,
            [
                t for t in transactions
                if t['type'] != 'transfer'
            ],
        )

    def get_transfers(self, currency):
        return self.get_transactions(currency, is_transfer=True)

    def get_transfers_parser(self, response, value_types):
        (currency, transactions) = response

        for t in transactions:
            t['currency'] = currency
            t['exchange'] = self.NAME
            t['details']['id'] = t.get('id', None)

        return [
            rename_keys_values(transaction, self.TRANSACTIONS_MAP, value_types)
            for transaction in transactions
        ]

    def get_fills(self, currency):
        return self.get_transactions(currency, is_transfer=False)

    def get_fills_parser(self, response, value_types):
        return self.get_transfers_parser(response, value_types)



