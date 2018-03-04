import json


class LiquiTransactionsResponse(object):
    def __init__(self):
        self.withdrawals_response = {
            u'Info': {u'IsSuccess': True, u'Errors': None, u'ServerTime': u'00:00:00.0011048', u'Time': u'00:00:00'},
            u'Value': [{u'Status': 5, u'Fee': 0.01, u'CurrencyId': 2,
                        u'Data': u'{\r\n  "Address": "LWKzpuu4LDc8NTtGRKZHLDor98c9PwAziw",\r\n  "Memo": "",\r\n  "Tx": "1b32b2c3dc27d92ea42ccf61de16f3c2633ddd9e8c94de4f2bb60f93de344d22",\r\n  "Error": null\r\n}',
                        u'Create': 1515193298, u'UserId': 43858, u'Amount': 6.67711055, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 515477}, {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 2,
                                         u'Data': u'{\r\n  "Address": "LQmG4veZbRoExbdwn5EGrg2uDN7iDtV3XE",\r\n  "Memo": "",\r\n  "Tx": "82073452d1224918f70d192a10da9d2dabd088d268d54c963505d95e0b5c2a8a",\r\n  "Error": null\r\n}',
                                         u'Create': 1514768393, u'UserId': 43858, u'Amount': 6.97308973,
                                         u'ConfirmType': 1, u'Type': 1, u'Id': 489997},
                       {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 2,
                        u'Data': u'{\r\n  "Address": "LMrx66GR8R7xYB39VHaY196W9RAZ2CBT2k",\r\n  "Memo": "",\r\n  "Tx": "e97d83cab10af707c47ade1aa2585f968c5379311821bc0cd0198fcf020de54a",\r\n  "Error": null\r\n}',
                        u'Create': 1514766757, u'UserId': 43858, u'Amount': 2.18665055, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 489958}, {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 12,
                                         u'Data': u'{\r\n  "Address": "0xD81809810c69AA576aB2c342C7AA1D6a729d5FFD",\r\n  "Memo": "",\r\n  "Tx": "0x0de6205b1b7e2633d40670f40d3956065b119dff8c8aa2f34fe27281be283066",\r\n  "Error": null\r\n}',
                                         u'Create': 1512687518, u'UserId': 43858, u'Amount': 2.6833092,
                                         u'ConfirmType': 1, u'Type': 1, u'Id': 431321},
                       {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 2,
                        u'Data': u'{\r\n  "Address": "LQnbBNs8D5zkwjodvLMVdcUjsbwqARDkKo",\r\n  "Memo": "",\r\n  "Tx": "a9219f934ea9b522b9860ca8efdfc33c7a9a03dc1ca03dc2f7a242ed9ad1b836",\r\n  "Error": null\r\n}',
                        u'Create': 1512686861, u'UserId': 43858, u'Amount': 14.66337186, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 431299}, {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 12,
                                         u'Data': u'{\r\n  "Address": "0x71F4Edac481E43f09695C33b9CAbBf6Cb16D987a",\r\n  "Memo": "",\r\n  "Tx": "0xc4c005392cc40d8ce4bc9c8e771d92027038bc54f3705abfcc50f52a8fbf3951",\r\n  "Error": null\r\n}',
                                         u'Create': 1510042236, u'UserId': 43858, u'Amount': 6.57858286,
                                         u'ConfirmType': 1, u'Type': 1, u'Id': 383224},
                       {u'Status': 5, u'Fee': 0.002, u'CurrencyId': 2,
                        u'Data': u'{\r\n  "Address": "LeKwEyCoQ8T7GbdZd56KJ4BzZjuDRvMuq7",\r\n  "Memo": "",\r\n  "Tx": "c613f419343847748f22d5e0e9852e1275519619584a38052bc40d75dadefcf2",\r\n  "Error": null\r\n}',
                        u'Create': 1508223684, u'UserId': 43858, u'Amount': 15.982, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 345552}, {u'Status': 5, u'Fee': 0.01, u'CurrencyId': 12,
                                         u'Data': u'{\r\n  "Address": "0x30bfa1c192efdd080614befb610466d10f723349",\r\n  "Memo": "",\r\n  "Tx": "0x3bed743a65c6ccbdeb7590d2d2b3cea364fbb371d625bc036b88db198fea00d2",\r\n  "Error": null\r\n}',
                                         u'Create': 1504631770, u'UserId': 43858, u'Amount': 0.49, u'ConfirmType': 1,
                                         u'Type': 1, u'Id': 246425}, {u'Status': 5, u'Fee': 3.0, u'CurrencyId': 18,
                                                                      u'Data': u'{\r\n  "Address": "0x6b8a104e3a105a93506a22c09052cd034546dab6",\r\n  "Memo": "",\r\n  "Tx": "0x7652b7f45182eaef44d7d2fb15dcc7f3b797c7b12648224e8ce1a57d9586ff6a",\r\n  "Error": null\r\n}',
                                                                      u'Create': 1504631676, u'UserId': 43858,
                                                                      u'Amount': 497.0, u'ConfirmType': 1, u'Type': 1,
                                                                      u'Id': 246420},
                       {u'Status': 5, u'Fee': 3.0, u'CurrencyId': 18,
                        u'Data': u'{\r\n  "Address": "0xd10e6d5328941b60ed53d07c31bb9b2f97304fc2",\r\n  "Memo": "",\r\n  "Tx": "0x12a462f12df1ced9fa9a49bb8a96aecfd01bcbde2fe157298709f8f8f6b036be",\r\n  "Error": null\r\n}',
                        u'Create': 1504631610, u'UserId': 43858, u'Amount': 497.0, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 246419}, {u'Status': 5, u'Fee': 3.0, u'CurrencyId': 35,
                                         u'Data': u'{\r\n  "Address": "12n1JLf74iLxZoxxrBDMQdBsneyaMGUKEi",\r\n  "Memo": "",\r\n  "Tx": "d9df23581504aabb5ccfbd4581a71f0ad22ac2485a8b09ffbc4f21c249b90d18",\r\n  "Error": null\r\n}',
                                         u'Create': 1504475761, u'UserId': 43858, u'Amount': 100.0, u'ConfirmType': 1,
                                         u'Type': 1, u'Id': 241905}, {u'Status': 5, u'Fee': 3.0, u'CurrencyId': 18,
                                                                      u'Data': u'{\r\n  "Address": "0xf4029920244f1f9b1d7ca8b8b51287617576af9b",\r\n  "Memo": "",\r\n  "Tx": "0xb653fcdb72b4e97f8ae6f8266bcd5eb70a25765607e0c0c9b0a0e60f97f5f352",\r\n  "Error": null\r\n}',
                                                                      u'Create': 1502772376, u'UserId': 43858,
                                                                      u'Amount': 100.0, u'ConfirmType': 1, u'Type': 1,
                                                                      u'Id': 181219},
                       {u'Status': 5, u'Fee': 3.0, u'CurrencyId': 18,
                        u'Data': u'{\r\n  "Address": "0x8f24f4b22436965971dff5ebcc514c4f06174a77",\r\n  "Memo": "",\r\n  "Tx": "0x1c8c4024686939b3aa9fba640d53bc2f566b5d3d8500efbd6edcc3bee1de583f",\r\n  "Error": null\r\n}',
                        u'Create': 1502772135, u'UserId': 43858, u'Amount': 600.0, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 181211}, {u'Status': 5, u'Fee': 0.0015, u'CurrencyId': 1,
                                         u'Data': u'{\r\n  "Address": "1Hu2AhhJmYEKJYzV6PP7A4qjyy3n8ebHmh",\r\n  "Memo": "",\r\n  "Tx": "15fe86e78dcbb1a4b6288c65406d2a5b6c8fb5b4d9aff71867c9353075abccc3",\r\n  "Error": null\r\n}',
                                         u'Create': 1502391545, u'UserId': 43858, u'Amount': 0.14971333,
                                         u'ConfirmType': 1, u'Type': 1, u'Id': 166756},
                       {u'Status': 5, u'Fee': 0.002, u'CurrencyId': 2,
                        u'Data': u'{\r\n  "Address": "LeLmWkzqnFdxsp5AtbujjKdtZA8Kn5rJ6Z",\r\n  "Memo": "",\r\n  "Tx": "6aceb5888f935694d806c519cbc7c4282118b63238b5f613bef0e9373ba6b787",\r\n  "Error": null\r\n}',
                        u'Create': 1501022019, u'UserId': 43858, u'Amount': 33.84776228, u'ConfirmType': 1, u'Type': 1,
                        u'Id': 146208}]}
        self.deposits_response = {
            "Info": {"IsSuccess": None, "ServerTime": "00:00:00.0009413", "Time": "00:00:00", "Errors": None},
            "Value": [
                {"Id": 312380, "UserId": 43858, "CurrencyId": 12, "Amount": 1.994, "Complete": 'true', "Time": 1505924542,
                 "Data": "{\r\n  \"TxKey\": \"0xb34497db0ce149226604b6ab35787d2bc9cd34848e8c4c13bbcbe10f6c5b0c61\",\r\n  \"Symbol\": \"ETH\",\r\n  \"Time\": 1505924433,\r\n  \"Address\": \"0x512748afe258b4b6002717a5638dd8b928360b06\",\r\n  \"From\": \"0x32be343b94f860124dc4fee278fdcbd38c102d88\",\r\n  \"Memo\": null,\r\n  \"Amount\": 1.994,\r\n  \"Confirmations\": 11,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0xb34497db0ce149226604b6ab35787d2bc9cd34848e8c4c13bbcbe10f6c5b0c61\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 180543, "UserId": 43858, "CurrencyId": 36, "Amount": 13.5, "Complete": 'true', "Time": 1502381285,
                 "Data": "{\r\n  \"TxKey\": \"0x5755a137d567237426629e56dec3c4acc7633ab4431f30d42a83877f665a7bc5\",\r\n  \"Symbol\": \"REP\",\r\n  \"Time\": 1502381269,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 13.5,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x5755a137d567237426629e56dec3c4acc7633ab4431f30d42a83877f665a7bc5\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 178942, "UserId": 43858, "CurrencyId": 12, "Amount": 1.72712461, "Complete": 'true',
                 "Time": 1502349765,
                 "Data": "{\r\n  \"TxKey\": \"0x178cb426794c06696f00c2d80ad819d7ab66c8168dbe4ce4644b8428adf6f61e\",\r\n  \"Symbol\": \"ETH\",\r\n  \"Time\": 1502349653,\r\n  \"Address\": \"0xfd856e7a1fde1c6e86312685d0ac418452eecb75\",\r\n  \"From\": null,\r\n  \"Memo\": null,\r\n  \"Amount\": 1.72712461,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x178cb426794c06696f00c2d80ad819d7ab66c8168dbe4ce4644b8428adf6f61e\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 163862, "UserId": 43858, "CurrencyId": 80, "Amount": 470.0, "Complete": 'true', "Time": 1501605071,
                 "Data": "{\r\n  \"TxKey\": \"0xb57f01b0801706ed84ba7ad5befad20ba3b0b0db255d9f71f0429fb07226a329\",\r\n  \"Symbol\": \"OAX\",\r\n  \"Time\": 1501605057,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 470.0,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0xb57f01b0801706ed84ba7ad5befad20ba3b0b0db255d9f71f0429fb07226a329\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 163848, "UserId": 43858, "CurrencyId": 57, "Amount": 1014.2, "Complete": 'true',
                 "Time": 1501602703,
                 "Data": "{\r\n  \"TxKey\": \"0xb43f84399123cc5cb8b5a3b8fbadc0fa9293c2d747d0e6338df5a881e3ec8236\",\r\n  \"Symbol\": \"MYST\",\r\n  \"Time\": 1501602698,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 1014.2,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0xb43f84399123cc5cb8b5a3b8fbadc0fa9293c2d747d0e6338df5a881e3ec8236\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 163846, "UserId": 43858, "CurrencyId": 51, "Amount": 2690.0, "Complete": 'true',
                 "Time": 1501602609,
                 "Data": "{\r\n  \"TxKey\": \"0x7a48856a7ecdd5016e6da0c5da4324b84f68fee8cfd225f1be62c40fcda9b582\",\r\n  \"Symbol\": \"BAT\",\r\n  \"Time\": 1501602597,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 2690.0,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x7a48856a7ecdd5016e6da0c5da4324b84f68fee8cfd225f1be62c40fcda9b582\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 154425, "UserId": 43858, "CurrencyId": 77, "Amount": 2500.0, "Complete": 'true',
                 "Time": 1500588627,
                 "Data": "{\r\n  \"TxKey\": \"0xeab175e6466450d5bfde9df039fb73c967a2d85a3d0920d1cebfd49e3c297270\",\r\n  \"Symbol\": \"CVC\",\r\n  \"Time\": 1500588622,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 2500.0,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0xeab175e6466450d5bfde9df039fb73c967a2d85a3d0920d1cebfd49e3c297270\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 154424, "UserId": 43858, "CurrencyId": 54, "Amount": 200.0, "Complete": 'true', "Time": 1500588562,
                 "Data": "{\r\n  \"TxKey\": \"0xe176cf17221335c7346e272b76058330cbfac5d4169410e2a2d61c922731e40d\",\r\n  \"Symbol\": \"BNT\",\r\n  \"Time\": 1500588548,\r\n  \"Address\": \"0xe06209a92feffd0b5639a4fffb680988be09c6da\",\r\n  \"From\": \"0xc4d69ddc6e3af2a81154a498b0b6c1a19eefc5b8\",\r\n  \"Memo\": null,\r\n  \"Amount\": 200.0,\r\n  \"Confirmations\": 10,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0xe176cf17221335c7346e272b76058330cbfac5d4169410e2a2d61c922731e40d\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 146206, "UserId": 43858, "CurrencyId": 12, "Amount": 1.79220496, "Complete": 'true',
                 "Time": 1499895729,
                 "Data": "{\r\n  \"TxKey\": \"0x839281495f4f6ebeae5fa1ead40e4671a174730a50e00596965ec3d1ac80d6f4\",\r\n  \"Symbol\": \"ETH\",\r\n  \"Time\": 1499895544,\r\n  \"Address\": \"0xfd856e7a1fde1c6e86312685d0ac418452eecb75\",\r\n  \"From\": null,\r\n  \"Memo\": null,\r\n  \"Amount\": 1.79220496,\r\n  \"Confirmations\": 11,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x839281495f4f6ebeae5fa1ead40e4671a174730a50e00596965ec3d1ac80d6f4\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 143002, "UserId": 43858, "CurrencyId": 1, "Amount": 0.22343715, "Complete": 'true',
                 "Time": 1499722963,
                 "Data": "{\r\n  \"TxKey\": \"8b6f0cdc9e0caabc687163606fc8fd29ea64c83db253c3cb25157665dbec24c5_12azUZHzuH7Y2AwGtaXUygQWkjkwBbTfSS\",\r\n  \"Symbol\": \"BTC\",\r\n  \"Time\": 1499721480,\r\n  \"Address\": \"12azUZHzuH7Y2AwGtaXUygQWkjkwBbTfSS\",\r\n  \"From\": null,\r\n  \"Memo\": null,\r\n  \"Amount\": 0.22343715,\r\n  \"Confirmations\": 2,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"8b6f0cdc9e0caabc687163606fc8fd29ea64c83db253c3cb25157665dbec24c5\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 137607, "UserId": 43858, "CurrencyId": 12, "Amount": 4.99958, "Complete": 'true',
                 "Time": 1499372048,
                 "Data": "{\r\n  \"TxKey\": \"0x8408e4ea728b905d74172068f340fa020a93fd7bb5c9fefd3ebf3c42d3addf2c\",\r\n  \"Symbol\": \"ETH\",\r\n  \"Time\": 1499371985,\r\n  \"Address\": \"0xfd856e7a1fde1c6e86312685d0ac418452eecb75\",\r\n  \"From\": null,\r\n  \"Memo\": null,\r\n  \"Amount\": 4.99958,\r\n  \"Confirmations\": 11,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x8408e4ea728b905d74172068f340fa020a93fd7bb5c9fefd3ebf3c42d3addf2c\",\r\n  \"CurrencyId\": 0\r\n}"},
                {"Id": 124883, "UserId": 43858, "CurrencyId": 12, "Amount": 4.99911248, "Complete": 'true',
                 "Time": 1498687134,
                 "Data": "{\r\n  \"TxKey\": \"0x45488edac32898512553ca658bbd88e8fb506e150d55fa61fc901de26efedf73\",\r\n  \"Symbol\": \"ETH\",\r\n  \"Time\": 1498687055,\r\n  \"Address\": \"0xfd856e7a1fde1c6e86312685d0ac418452eecb75\",\r\n  \"From\": null,\r\n  \"Memo\": null,\r\n  \"Amount\": 4.99911248,\r\n  \"Confirmations\": 13,\r\n  \"UserId\": 43858,\r\n  \"TxHash\": \"0x45488edac32898512553ca658bbd88e8fb506e150d55fa61fc901de26efedf73\",\r\n  \"CurrencyId\": 0\r\n}"}]}

    def _parse_response(self, response):
        parsed = response.copy()
        response_values = parsed.pop('Value')
        parsed_values = []

        for data in response_values:
            parsed_data = data.copy()
            blockchain_data = parsed_data.pop('Data')
            parsed_data.update(json.loads(blockchain_data.replace('\r\n', '').replace(' ', '')))
            parsed_values.append(parsed_data)

        parsed['Value'] = parsed_values

        return parsed

    def parse_withdrawals(self):
        return self._parse_response(self.withdrawals_response)

    def parse_deposits(self):
        return self._parse_response(self.deposits_response)

    def filter(self, response, currency_id):
        filtered = response.copy()
        values = filtered.pop('Value')
        filtered['Value'] = [v for v in values if v['CurrencyId'] == currency_id]

        return filtered

    def withdrawals(self, currency_id=None):
        response = self.parse_withdrawals()

        if currency_id is None:
            return response

        return self.filter(response, currency_id=currency_id)

    def deposits(self, currency_id=None):
        response = self.parse_deposits()

        if currency_id is None:
            return response

        return self.filter(response, currency_id=currency_id)


response = LiquiTransactionsResponse()


def withdrawals_response(currency_id=None):
    return response.withdrawals(currency_id=currency_id)


def deposits_response(currency_id=None):
    return response.deposits(currency_id=currency_id)


if __name__ == '__main__':
    import pdb

    pdb.set_trace()
