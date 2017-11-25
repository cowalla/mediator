request_url = 'https://api.gdax.com/products/{id}/ticker'


def response(id):
    eth_btc_response = {"trade_id": 2033258, "price": "0.05397000", "size": "0.13655845", "bid": "0.05396",
                        "ask": "0.05397",
                        "volume": "62778.70074449", "time": "2017-11-25T20:55:50.641000Z"}
    ltc_btc_response = {"trade_id": 1322617, "price": "0.00982000", "size": "8.19457433", "bid": "0.00981",
                        "ask": "0.00982", "volume": "105713.56125772", "time": "2017-11-25T20:59:29.831000Z"}
    btc_usd_response = {"trade_id": 24974590, "price": "8741.95000000", "size": "0.00000114", "bid": "8741.94",
                        "ask": "8741.95", "volume": "16332.32955146", "time": "2017-11-25T21:00:42.188000Z"}
    eth_usd_response = {"trade_id": 17097271, "price": "473.08000000", "size": "0.00210748", "bid": "473.07",
                        "ask": "473.08", "volume": "298761.62777390", "time": "2017-11-25T21:01:33.066000Z"}
    ltc_usd_response = {"trade_id": 12341664, "price": "85.96000000", "size": "7.00000000", "bid": "85.96",
                        "ask": "85.97", "volume": "905872.50264539", "time": "2017-11-25T21:01:15.296000Z"}

    return {
        'eth-btc': eth_btc_response,
        'ltc-btc': ltc_btc_response,
        'btc-usd': btc_usd_response,
        'eth-usd': eth_usd_response,
        'ltc-usd': ltc_usd_response,
    }.get(id.lower(), {})
