from gdax import AuthenticatedClient as GDAXAuthenticatedClient, PublicClient as GDAXPublicClient

from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys
from crypto_mediator.settings import GDAX


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

