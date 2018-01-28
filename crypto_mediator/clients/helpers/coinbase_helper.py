from coinbase.wallet.client import Client as CoinbaseClient

from crypto_mediator.clients.helpers.helper import ClientHelper, percent_difference, to_datetime
from crypto_mediator.settings import COINBASE


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

