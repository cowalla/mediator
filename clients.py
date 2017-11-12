from exchanges import GDAXClientHelper, LiquiClientHelper, PoloniexClientHelper

# exchange choices
GDAX = 'gdax'
LIQUI = 'liqui'
POLONIEX = 'poloniex'


helper_map = {
    GDAX: GDAXClientHelper,
    LIQUI: LiquiClientHelper,
    POLONIEX: LiquiClientHelper,
}



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
    def __init__(self, **client_credentials):
        super(MetaClient, self).__init__()

        self.helpers = {}

        for client, credentials in client_credentials.iteritems():
            HelperClass = helper_map.get(client)

            if HelperClass is None:
                raise NotImplementedError('{} is not implimented!'.format(client))

            self.helpers[client] = HelperClass(**credentials)


    def ticker(self, exchange, pairs):
        """
        Given an exchange, returns the ticker for the pairs given
        """
        helper = self.helpers[exchange]

        return helper.ticker(pairs)


# Overlays for each supported client

