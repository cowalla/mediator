import datetime
import json
import logging
import time
from operator import attrgetter

logging.basicConfig(filename='logs/{}'.format(time.time()), level=logging.DEBUG)
logger = logging.getLogger('MarketClient')


def timestamp_to_datetime(ts):
  return datetime.datetime.utcfromtimestamp(ts / 1000)


def downcase(function):
  """
  Downcases the output of a function acting on a client.

  :param mc: MasterClient instance. Might be useful later.
  """

  def wrapper(mc, client, **kwargs):
    data = function(mc, client, **kwargs)

    return json.loads(json.dumps(data).lower())

  return wrapper


def no_cache(function):
  """
  Tells the endpoint not to cache the response by adding a "no_cache" kwarg.

  :param mc: MasterClient instance. Might be useful later.
  """

  def wrapper(mc, client, *args, **kwargs):
    kwargs.update({'no_cache': True})

    return function(mc, client, *args, **kwargs)

  return wrapper


def retry(func):
  def retried_func(*args, **kwargs):

    tries = 0

    result = None
    while result is None:
      try:
        result = func(*args, **kwargs)
      except:
        time.sleep(1)
        tries += 1
        if tries % 7 == 0:
          print "There seems to be a problem with %s" % func.__name__
          print result
          return result
    return result

  return retried_func


class MarketClient(object):
  """
  A layer of abstraction over disparate clients for exchanges to make them all work the same.
  """

  def __init__(self, clients):
    self.populated = False  # flag to keep track if the cache has values
    self.clients = clients
    self.cache = {
      exchange: {
        'currencies': {'values': None, 'timestamp': None},
        'pairs': {'values': None, 'timestamp': None},
        'offers': {'values': None, 'timestamp': None},
        'balances': {'values': None, 'timestamp': None}
      }
      for exchange in self.clients.keys()
      }

  def refresh_cache(self, fname=None):
    if fname is not None:
      try:
        api_functions = [getattr(self, fname)]
      except AttributeError:
        print 'No function named {}'.format(fname)
        raise APIError('Refresh cache failed')
    else:
      api_functions = [self.get_currencies, self.get_pairs, self.get_offers, self.get_balances]

    for exchange in self.clients.keys():
      for api_function in api_functions:
        api_function(exchange)

    self.populated = True

  def get_fiat_pairs(self, exchange, fiat=None):
    if not self.populated:
      self.get_pairs(exchange)

    all_pairs = self.cache[exchange]['pairs']['values']

    return [
      p
      for p in all_pairs
      if fiat in p
      ]

  def get_fiat_ticker(self, exchange, fiat='usdt'):
    pairs = self.get_fiat_pairs(exchange, fiat=fiat)

    if exchange == 'poloniex':
      self._poloniex_get_pairs(self.clients['poloniex'])
      pairs = self.cache['poloniex']['pairs']

    joined_pairs = '-'.join(pairs)

    return self.get_ticker(exchange, pairs_str=joined_pairs)

  def get_ticker(self, exchange, pairs_str):
    return self._do_request(exchange, 'ticker', pairs_str=pairs_str)

  def get_currencies(self, exchange):
    """
    returns a list of tradeable currencies traded on the exchange

    e.g. ['btc', 'eth', 'ltc', ... ]
    """
    return self._do_request(exchange, 'currencies')

  def get_pairs(self, exchange):
    """
    returns a list of tradable currency pairs

    e.g. ['ltc_btc', 'ltc_eth', 'ltc_usdt', ... ]
    """
    return self._do_request(exchange, 'pairs')

  def get_offers(self, exchange):
    """
    returns a dictionary of {fiat: {currency: {'asks': [Offer, Offer], 'bids': [Offer]}, currency: { ...

    e.g. ['btc': {'eth': {'asks': [Offer, Offer] 'bids': [Offer, Offer]}, 'ltc': {'asks': [ ... ], ... ]
    """
    return self._do_request(exchange, 'offers')

  # Requires authentication
  def get_my_active_orders(self, exchange):
    """
    returns all active orders for the account
    """
    return self._do_request(exchange, 'my_active_orders')

  def get_balances(self, exchange):
    return self._do_request(exchange, 'balances')

  def post_cancel_order(self, exchange, order_id):
    logging.info('post_cancel_order({}, {})'.format(exchange, order_id))
    return self._do_request(exchange, 'cancel_order', method='post', order_id=order_id)

  def post_create_sell_order(self, exchange, currency, fiat, rate, amount):
    msg = 'post_create_sell_order({}, {}, {}, {}, {})'.format(
      exchange,
      currency,
      fiat,
      rate,
      amount,
    )
    logging.info(msg)
    return self._do_request(
      exchange,
      'create_sell_order',
      method='post',
      currency=currency,
      fiat=fiat,
      rate=rate,
      amount=amount
    )

  def post_create_buy_order(self, exchange, currency, fiat, rate, amount):
    msg = 'post_create_buy_order({}, {}, {}, {}, {})'.format(
      exchange,
      currency,
      fiat,
      rate,
      amount,
    )
    logging.info(msg)

    return self._do_request(
      exchange,
      'create_buy_order',
      method='post',
      currency=currency,
      fiat=fiat,
      rate=rate,
      amount=amount,
    )

  def post_withdraw(self, exchange, address, currency, amount):
    logging.info('post_withdraw({}, {}, {}, {})'.format(exchange, address, currency, amount))

    return self._do_request(
      exchange,
      'withdraw',
      method='post',
      address=address,
      currency=currency,
      amount=amount,
    )

  def _get_trading_pair(self, exchange, fiat, currency):
    if not self.populated:
      self.refresh_cache(fname='get_pairs')

    pairs = self.cache[exchange]['pairs']['values']
    return [p for p in pairs if fiat in p and currency in p][0]

  # Liqui

  @downcase
  def _liqui_get_ticker(self, client, pairs_str):
    return client.ticker(pair=pairs_str)

  @downcase
  def _liqui_get_currencies(self, client):
    return client.get_info()['funds'].keys()

  @downcase
  def _liqui_get_pairs(self, client):
    return client.info()['pairs'].keys()

  def _liqui_get_offers(self, client):
    offers = self.__liqui_get_offers(client)
    response = {}

    for currency_pair, offers_dict in offers.iteritems():
      currency, fiat = currency_pair.split('_')  # may not be the case
      self._add_currency_offers(response, offers_dict, currency, fiat, 'liqui')

    return response

  @downcase
  def __liqui_get_offers(self, client):
    # super secret method for getting raw data then downcasing it
    pairs = self._liqui_get_pairs(client)

    return client.depth('-'.join(pairs))

  def _liqui_get_my_active_orders(self, client):
    offers = self.__liqui_get_my_active_orders(client)

    return [
      ActiveOffer(
        id=pk,
        rate=o['rate'],
        amount=o['amount'],
        currency=o['pair'].split('_')[0],
        fiat=o['pair'].split('_')[1],
        created_at=o['timestamp_created'],
        type=o['type'],
        status=o['status'],
        exchange='liqui'
      )
      for pk, o in offers.iteritems()
      ]

  @downcase
  def __liqui_get_my_active_orders(self, client):
    return client.active_orders()

  @downcase
  def _liqui_get_balances(self, client):
    return client.balances()

  @downcase
  @no_cache
  def _liqui_post_cancel_order(self, client, order_id, **kwargs):
    return client.cancel_order(order_id=order_id)

  @downcase
  @no_cache
  @retry
  def _liqui_post_create_buy_order(self, client, currency, fiat, rate, amount, **kwargs):
    pair = self._get_trading_pair('liqui', fiat, currency)

    return client.buy(pair=pair, rate=rate, amount=amount)

  @downcase
  @no_cache
  @retry
  def _liqui_post_create_sell_order(self, client, currency, fiat, rate, amount, **kwargs):
    pair = self._get_trading_pair('liqui', fiat, currency)

    return client.sell(pair=pair, rate=rate, amount=amount)

  def _liqui_post_withdraw(self, client, address, currency, amount):
    params = {
      'coinName': currency,
      'amount': amount,
      'address': address,
    }

    return client._tapi(method='WithdrawCoin', **params)

  # Poloniex

  @downcase
  def _poloniex_get_currencies(self, client):
    return client.returnCurrencies().keys()

  @downcase
  def _poloniex_get_ticker(self, client, pairs_str):
    if not self.populated:
      self._poloniex_get_pairs(client)

    return self.cache['poloniex']['get_pairs'][pairs_str]

  @downcase
  def _poloniex_get_pairs(self, client):
    return client.returnTicker().keys()

  def _poloniex_get_offers(self, client):
    offers = self.__poloniex_get_offers(client)
    response = {}

    for currency_pair, offers_dict in offers.iteritems():
      fiat, currency = currency_pair.split('_')  # may not be the case
      self._add_currency_offers(response, offers_dict, currency, fiat, 'poloniex')

    return response

  @downcase
  def __poloniex_get_offers(self, client):
    # super secret method for getting raw data then downcasing it
    return client.returnOrderBook()

  def _poloniex_get_my_active_orders(self, client):
    offers_dict = self.__poloniex_get_my_active_orders(client)
    my_active_orders = []

    for pair, offers_list in offers_dict.iteritems():
      [fiat, currency] = pair.split('_')

      if len(offers_list) is 0:
        continue

      my_active_orders += [
        ActiveOffer(
          fiat=fiat,
          currency=currency,
          id=o['orderNumber'],
          rate=o['rate'],
          amount=o['amount'],
          type=o['type'],
          exchange='poloniex'
        )
        for o in offers_list
        ]

    return my_active_orders

  @downcase
  def __poloniex_get_my_active_orders(self, client):
    return client.returnOpenOrders(currencyPair='all')

  @downcase
  def _poloniex_get_balances(self, client):
    return {k: float(v) for k, v in client.returnBalances().iteritems()}

  @downcase
  @no_cache
  def _poloniex_post_cancel_order(self, client, order_id, **kwargs):
    response = client.cancelOrder(orderNumber=order_id)

    if response.get('success') is not 1:
      raise PoloniexError('Was not successful in canceling order {}'.format(order_id))

  @downcase
  @no_cache
  def _poloniex_post_create_buy_order(self, client, currency, fiat, rate, amount, **kwargs):
    # TODO: explore order_types e.g. 'immediateOrCancel'
    pair = self._get_trading_pair('poloniex', fiat, currency).upper()

    return client.buy(currencyPair=pair, rate=rate, amount=amount)

  @downcase
  @no_cache
  def _poloniex_post_create_sell_order(self, client, currency, fiat, rate, amount, **kwargs):
    # TODO: explore order_types e.g. 'immediateOrCancel'
    pair = self._get_trading_pair('poloniex', fiat, currency).upper()

    return client.sell(currencyPair=pair, rate=rate, amount=amount)

  @downcase
  def _poloniex_post_withdraw(self, client, address, currency, amount):
    return client.withdraw(currency=currency, address=address, amount=amount)

  # GDAX

  @downcase
  def _gdax_get_ticker(self, client, pairs_str):
    return client.ticker(pair=pairs_str)

  @downcase
  def _gdax_get_currencies(self, client):
    return client.get_info()['funds'].keys()

  @downcase
  def _gdax_get_pairs(self, client):
    return client.get_products()

  def _gdax_get_offers(self, client):
    offers = self.__gdax_get_offers(client)
    response = {}

    for currency_pair, offers_dict in offers.iteritems():
      currency, fiat = currency_pair.split('_')  # may not be the case
      self._add_currency_offers(response, offers_dict, currency, fiat, 'gdax')

    return response

  @downcase
  def __gdax_get_offers(self, client):
    # super secret method for getting raw data then downcasing it
    pairs = self._gdax_get_pairs(client)

    return client.depth('-'.join(pairs))

  def _gdax_get_my_active_orders(self, client):
    offers = self.__gdax_get_my_active_orders(client)

    return [
      ActiveOffer(
        id=pk,
        rate=o['rate'],
        amount=o['amount'],
        currency=o['pair'].split('_')[0],
        fiat=o['pair'].split('_')[1],
        created_at=o['timestamp_created'],
        type=o['type'],
        status=o['status'],
        exchange='gdax'
      )
      for pk, o in offers.iteritems()
      ]

  @downcase
  def __gdax_get_my_active_orders(self, client):
    return client.active_orders()

  @downcase
  def _gdax_get_balances(self, client):
    return client.balances()

  @downcase
  @no_cache
  def _gdax_post_cancel_order(self, client, order_id, **kwargs):
    return client.cancel_order(order_id=order_id)

  @downcase
  @no_cache
  def _gdax_post_create_buy_order(self, client, currency, fiat, rate, amount, **kwargs):
    pair = self._get_trading_pair('gdax', fiat, currency)

    return client.buy(pair=pair, rate=rate, amount=amount)

  @downcase
  @no_cache
  def _gdax_post_create_sell_order(self, client, currency, fiat, rate, amount, **kwargs):
    pair = self._get_trading_pair('gdax', fiat, currency)

    return client.sell(pair=pair, rate=rate, amount=amount)

  def _gdax_post_withdraw(self, client, address, currency, amount):
    params = {
      'coinName': currency,
      'amount': amount,
      'address': address,
    }

    return client._tapi(method='WithdrawCoin', **params)

  # helper functions

  def _add_currency_offers(self, response, offers_dict, currency, fiat, exchange):
    """
    Adds offers from offers_dict to response
    """
    currency_offers = {'asks': [], 'bids': [], 'ask': None, 'bid': None}

    if response.get(fiat, {}).get(currency) is not None:
      raise APIError('Currency "{}" has already been populated!'.format(currency))

    for offer_type, offer_list in offers_dict.iteritems():
      if offer_type not in currency_offers:  # throw away metadata
        continue

      offer_object_list = []

      for offer in offer_list:
        offer_kwargs = {
          'rate': float(offer[0]),
          'amount': float(offer[1]),
          'exchange': exchange,
          'fiat': fiat,
          'currency': currency,
        }

        if offer_type == 'bids':
          o = Sell(**offer_kwargs)
        elif offer_type == 'asks':
          o = Buy(**offer_kwargs)
        else:
          continue

        offer_object_list.append(o)

      if offer_type == 'asks' and offer_object_list:
        currency_offers['ask'] = min(offer_object_list, key=attrgetter('rate'))
      elif offer_type == 'bids' and offer_object_list:
        currency_offers['bid'] = max(offer_object_list, key=attrgetter('rate'))

      currency_offers[offer_type] = offer_object_list

    if response.get(fiat) is None:
      response[fiat] = {}

    response[fiat][currency] = currency_offers

  def _timestamp(self):
    # For marking cached items
    return time.time()

  def _get_endpoint_for_exchange(self, exchange, endpoint, method):
    """
    methods for each exchange follow a naming convention to make this client agnostic.
    """
    function_name = '_{exchange}_{method}_{endpoint}'.format(
      exchange=exchange,
      endpoint=endpoint,
      method=method,
    )

    try:
      f = getattr(self, function_name)
      client = self.clients[exchange]
    except (AttributeError, KeyError) as e:
      print e
      raise NotImplementedError('No function found named "{}"'.format(function_name))

    return f, client

  @retry
  def _handle_request(self, function, client, exchange, endpoint, method, *args, **kwargs):
    """
    Buffer to do any requests handling that may be necessary
    """
    msg_lines = [
      '[REQUEST]',
      'function: {}'.format(str(function)),
      'client: {}'.format(str(client)),
      'exchange: {}'.format(exchange),
      'endpoint: {}'.format(endpoint),
      'method: {}'.format(method),
      '*args: {}'.format(str(list(*args))),
      '**kwargs: {}'.format(str(dict(**kwargs))),
    ]
    logger.info('\n{message}\n'.format(message='\n'.join(msg_lines)))

    response = function(client, *args, **kwargs)

    if not kwargs.get('no_cache'):
      self._cache_response(response, exchange, endpoint, method)

    return response

  def _cache_response(self, response, exchange, endpoint, method):
    """
    writes last api responses to a in-memory cache
    """
    self.cache[exchange][endpoint] = {'values': response, 'timestamp': self._timestamp()}

  def _do_request(self, exchange, endpoint, method='get', **kwargs):
    if exchange not in self.clients:
      raise NotImplementedError('Exchange "{}" is not supported'.format(exchange))

    f, client = self._get_endpoint_for_exchange(exchange, endpoint, method=method)

    return self._handle_request(f, client, exchange, endpoint, method, **kwargs)


class APIError(ValueError):
  pass


class PoloniexError(APIError):
  pass


class LiquiError(APIError):
  pass
