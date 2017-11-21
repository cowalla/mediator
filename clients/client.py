import json

from clients.helpers import GDAXClientHelper, LiquiClientHelper, PoloniexClientHelper
from settings import GDAX, LIQUI, POLONIEX


class DowncaseError(SyntaxError):
    pass

def downcase(function):
    """
    Downcases the output of a function acting on a client.
    """
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)

        try:
            return json.loads(json.dumps(data).lower())
        except:
            msg = (
                'Could not downcase function with '
                'args: {}, '
                'kwargs: {}'
            ).format(str(args), str(kwargs))

            raise DowncaseError(msg)

    return wrapper


class MetaClient(object):
    """
    Interacts with cryptocurrency market clients to,
     - standardize interactions
     - easily interact with multiple clients
     - trade across multiple exchanges

    expects client credentials in the form,
        exchange: {
          key: ...,
          secret: ...,
    """
    HELPER_MAP = {
        GDAX: GDAXClientHelper,
        LIQUI: LiquiClientHelper,
        POLONIEX: PoloniexClientHelper,
    }


    def __init__(self, **exchange_kwargs):
        super(MetaClient, self).__init__()

        self.helpers = {}

        for exchange, kwargs in exchange_kwargs.iteritems():
            HelperClass = self.HELPER_MAP.get(exchange)

            if HelperClass is None:
                raise NotImplementedError('{} is not implemented!'.format(exchange))

            self.helpers[exchange] = HelperClass(**kwargs)


    @downcase
    def ticker(self, exchange, pairs):
        """
        Given an exchange, returns the ticker for the pairs given
        """
        helper = self.helpers[exchange]

        return helper.get_ticker(pairs)

    @downcase
    def pairs(self, exchange, pairs):
        """
        Given an exchange, returns the ticker for the pairs given
        """
        helper = self.helpers[exchange]

        return helper.get_pairs(pairs)


# Overlays for each supported client

