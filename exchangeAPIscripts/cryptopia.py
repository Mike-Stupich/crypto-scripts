"""
    wrapper for using Cryptopia.co.nz API
"""

import time
import hmac
import urllib
import requests
import hashlib
import base64
import sys
import json




PUBLIC_SET = {'GetCurrencies', 'GetTradePairs', 'GetMarkets', 'GetMarketHistory', 'GetMarketOrders'}
PRIVATE_SET = {'GetBalance', 'GetDepositAddress', 'GetOpenOrders', 'GetTradeHistory', 'GetTransactions', 'SubmitTrade', 'CancelTrade', 'SubmitTip', 'SubmitWithdraw'}
BASE_URL = "https://www.cryptopia.co.nz/api/"
class Cryptopia(object):
    """
        Used for requesting Cryptopia with API key and API secret
    """
    def __init__(self, api_key, api_secret):
        self.api_key = str(api_key) if api_key is not None else ''
        self.api_secret = str(api_secret) if api_secret is not None else ''

    def api_query(self, method, options=None):
        """
            Query Cryptopia with given method and options
        """
        req_url = BASE_URL + method

        if method in PUBLIC_SET:
            if options:
                for param in options:
                    req_url += '/' + str(param)
            request = requests.get(req_url)

        elif method in PRIVATE_SET:
            nonce = str(int(time.time()))
            post_data = json.dumps(options)
            md5 = hashlib.md5()
            md5.update(post_data)
            options_as_base_64 = base64.b64encode(md5.digest())
            req = self.api_key + "POST" + urllib.quote_plus(req_url).lower() + nonce + options_as_base_64
            hmac_sig = base64.b64encode(hmac.new(base64.b64decode(self.api_secret), req, hashlib.sha256).digest())
            header_val = "amx " + self.api_key + ":" + hmac_sig + ":" + nonce
            headers = {'Authorization': header_val, 'Content-Type': 'application/json; charset=utf-8' }
            request = requests.post(req_url, data = post_data, headers = headers)
        
        return request.text
