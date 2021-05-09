# Deprecated. Gatecoin doesn't exist anymore.

import requests


class GatecoinClient:
    API_URL = 'api.gatecoin.com'
    PUBLIC_API_URL = 'https://{host}/public/'.format(host=API_URL)
    TICKER_ROUTE = PUBLIC_API_URL + 'livetickers'

    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret

    def livetickers(self):
        response = requests.get(self.TICKER_ROUTE)

        return response.json()
