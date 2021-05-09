from collections import defaultdict

from coinbase.wallet.client import Client as CoinbaseClient

from crypto_mediator.clients.helpers.helper import ClientHelper, percent_difference, to_datetime, flatten, rename_keys_values
from crypto_mediator.settings import COINBASE


class CoinbaseClientHelperError(BaseException):
    pass


class CoinbaseClientHelper(ClientHelper):
    TRANSACTIONS_MAP = {
        'amount': ('amount', 'amount'),
        'currency': ('amount', 'currency'),
        'created': ('created_at',),
        'description': ('description',),
        'details': ('details',),
        'fee': ('network', 'transaction_fee', 'amount'),
        'from': ('from', 'address'),
        'txhash': ('network', 'hash'),
        'to': ('to', 'address'),
    }

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

    def _get_coinbase_transactions(self, currency):
        account_id = self.currency_account_id_map[currency]

        return self.client.get_transactions(account_id).data


    def mediator_transaction(self, transaction):
        return {
            'amount': float(transaction.amount.amount),
            'created': to_datetime(transaction.created_at),
            'currency': transaction.amount.currency.lower(),
            'txhash': transaction.network['hash'] if transaction.network else None,
            'exchange': self.NAME,
        }

    def get_transfers(self, currency, as_coinbasepro=True):
        # gets only coinbase transactions (not coinbasepro transfers)
        transactions = self._get_coinbase_transactions(currency)
        transactions_by_amount = self._transfers_by_amount(transactions)
        # If there's a paired withdrawal to a deposit, it's probably a coinbasepro transfer
        non_coinbasepro_transactions = [
            value['withdraw'] or value['deposit']
            for value in transactions_by_amount.values()
            if bool(value['withdraw']) != bool(value['deposit']) # XOR
        ]

        if not as_coinbasepro:
            return non_coinbasepro_transactions

        coinbasepro_transactions = [
            (value['withdraw'], value['deposit'])
            for value in transactions_by_amount.values()
            if value['withdraw'] and value['deposit']  # and
        ]
        coinbase_transactions_for_coinbasepro = []

        for (withdraw, deposit) in coinbasepro_transactions:
            if withdraw['type'] == 'exchange_deposit':
                # deposit came from outside, going into coinbasepro
                coinbase_transactions_for_coinbasepro.append(deposit)
            else:
                # deposit came from coinbasepro, meaning it's a withdrawal from coinbase
                coinbase_transactions_for_coinbasepro.append(withdraw)

        return non_coinbasepro_transactions + coinbase_transactions_for_coinbasepro


    def get_transfers_parser(self, response, value_types):
        return [
            rename_keys_values(
                transaction,
                self.TRANSACTIONS_MAP,
                value_types,
                exchange_name=self.NAME,
                should_be_filled=False
            )
            for transaction in response
        ]

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
            for currency, account in self.accounts.items()
        }
        # set id map
        self.currency_account_id_map = {
            currency: self.accounts[currency].id
            for currency in self.currencies
        }

    def _transfers_by_amount(self, transactions):
        # finds transactions pairs that pass through to coinbasepro (received, sent),
        # requires transactions to be sorted by date
        def get_amount(transaction):
            amount = transaction.amount.amount
            network_amount = transaction.get('network', {}).get('transaction_amount', {})

            if network_amount:
                amount = network_amount.amount
            return str(amount)

        def is_withdraw(transaction):
            return get_amount(transaction).startswith('-')

        deposit_withdrawals = defaultdict(lambda: {'withdraw': None, 'deposit': None})

        for transaction in transactions:
            amount = get_amount(transaction).lstrip('-')

            if is_withdraw(transaction):
                deposit_withdrawals[amount]['withdraw'] = transaction
            else:
                deposit_withdrawals[amount]['deposit'] = transaction

        return deposit_withdrawals
