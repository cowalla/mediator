# Depricated. Liqui doesn't exist anymore.

from collections import defaultdict
from liqui import Liqui as LiquiClient

from crypto_mediator.clients.helpers.helper import ClientError, ClientHelper, rename_keys_values
from crypto_mediator.settings import LIQUI


class LiquiClientHelper(ClientHelper):
    TICKER_MAP = {
        'last': ('last', ),
        'highest_bid': ('buy', ),
        'lowest_ask': ('sell', ),
        'base_volume': ('vol', ),
        'current_volume': ('vol_cur', ),
        'high': ('high', ),
        'low': ('low', ),
        'updated': ('updated', ),
        'average': ('avg', ),
    }
    TRANSACTIONS_MAP = {
        'fee': ('Fee', ),
        'txhash': ('Tx', ),
        'created': ('Create', ),
        'amount': ('Amount', ),
        'details': ('Memo', ),
        'currency': ('Currency', ),
        'to': ('To', ),
        'from': ('From', ),
        'type': ('Type', ),
    }

    NAME = LIQUI
    CLIENT_CLASS = LiquiClient

    def __init__(self, *args, **kwargs):
        super(LiquiClientHelper, self).__init__(*args, **kwargs)

        self.id_currency_map = self._get_id_currency_map()
        self.currency_id_map = {currency: c_id for c_id, currency in self.id_currency_map.items()}

    # public methods

    def get_ticker(self):
        all_liqui_pairs = [self._to_client_pair(p) for p in self.pairs]
        pair = '-'.join(all_liqui_pairs)
        ticker_response = self.client.ticker(pair=pair)

        if ticker_response.get('error'):
            raise ClientError(ticker_response['error'])

        return ticker_response

    def get_ticker_parser(self, response, value_types):
        parsed = {}

        for pair, data in response.items():
            mediator_pair = self.mediator_pair(pair)
            parsed_ticker_value = rename_keys_values(data, self.TICKER_MAP, value_types)
            parsed[mediator_pair] = parsed_ticker_value

        return parsed


    def get_currencies(self):
        pairs = self.get_pairs()

        return self._get_currencies_from_mediator_pairs(pairs)

    def get_currency_info(self):
        from crypto_mediator.fixtures.liqui.currency_info import response

        return response

    # account information

    def trade_history(self, batched=True, **params):
        response = self.client.trade_history(**params)
        trades = response.values()

        for trade in trades:
            trade['pair'] = self.mediator_pair(trade['pair'])

        if batched:
            trades = [
                self._batch_order(trades)
                for trades in self._batch_by_order_id(trades).values()
            ]

        return sorted(trades, key=lambda x: x['timestamp'])

    def _batch_by_order_id(self, trades):
        orders_dict = defaultdict(list)

        for trade in trades:
            orders_dict[trade['order_id']].append(trade)

        return orders_dict

    def _batch_order(self, trades):
        # use first trade as scaffold for batched order
        order = min(trades, key=lambda x: x['timestamp']).copy()
        fields_to_remove = ['trade_id', 'rate', 'is_your_order']

        for field in fields_to_remove:
            order.pop(field)

        total_amount = 0
        total_cost = 0

        for trade in trades:
            trade_amount = trade['amount']
            trade_cost = trade_amount * trade['rate']

            total_amount += trade_amount
            total_cost += trade_cost

        order.update(
            {
                'amount': total_amount,
                'rate': total_cost / float(total_amount),
            }
        )

        return order

    def get_withdrawals(self, currency=None):
        from crypto_mediator.fixtures.liqui.transactions import withdrawals_response

        currency_id = self.currency_id_map[currency] if currency is not None else None

        return withdrawals_response(currency_id)

    def get_deposits(self, currency=None):
        from crypto_mediator.fixtures.liqui.transactions import deposits_response

        currency_id = self.currency_id_map[currency] if currency is not None else None

        return deposits_response(currency_id)

    def get_transfers(self, currency=None):
        deposits = self.get_deposits(currency)['Value']

        for d in deposits:
            d['Type'] = 'deposit'
            d['From'] = d.pop('Address')

        withdrawals = self.get_withdrawals(currency)['Value']

        for w in withdrawals:
            w['Type'] = 'withdrawal'
            w['To'] = w.pop('Address')

        return deposits + withdrawals

    def get_transfers_parser(self, response, value_types):
        for t in response:
            currency_id = t.pop('CurrencyId')
            t['Currency'] = self.id_currency_map[currency_id]

        transactions = [
            rename_keys_values(
                transaction,
                self.TRANSACTIONS_MAP,
                value_types,
                exchange_name=self.NAME,
                should_be_filled=False,
            )
            for transaction in response
        ]

        return transactions

    def _get_client_pairs(self):
        return self.client.info()['pairs'].keys()

    def _get_id_currency_map(self):
        currency_info = self.get_currency_info()

        return {
            currency['Id']: currency['Symbol'].lower()
            for currency in currency_info
        }
