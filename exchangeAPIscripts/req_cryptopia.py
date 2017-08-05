import json
import time
import smtplib

from cryptopia import Cryptopia

class reqCryptopia():
    """
    Class to make requests to Cryptopia object.
    """
    def __init__(self):
        with open("apikeys.json") as apikeys:
            self.keys = json.load(apikeys)
            apikeys.close()
        for key in self.keys['APIs']:
            if key['exchange'] =='Cryptopia':
                self.cryptopia = Cryptopia(key['key'], key['secret'])


    def call_withdraw(self, currency, addr, payid, amount):
        """
        Input:
        Currency: The currency symbol of the coins to withdraw e.g. 'DOT' (not required if 'CurrencyId' supplied)
        CurrencyId: The Cryptopia currency identifier of the coins to withdraw e.g. '2' (not required if 'Currency' supplied)
        Address: The address to send the currency too. (Address must exist in you AddressBook, can be found in you Security settings page.)
        PaymentId: The unique paimentid to identify the payment. (PaymentId for CryptoNote coins.)
        Amount: the amount of coins to withdraw e.g. 123.00000000
        """
        print(addr)
        return self.cryptopia.api_query("SubmitWithdraw", {'Currency':currency, 'Address':addr, 'PaymentId':payid, 'Amount':amount})
    
    def get_balance_of_coin(self, currency):
        """
        Get balance of specific coin
        """
        return self.cryptopia.api_query('GetBalance', {'Currency':currency})
        


    def handle_withdraw(self, coin, addr, amount=None):
        """
        Handles withdraw of amount of coin to address
        """
        print(addr)
        balance = json.loads(self.get_balance_of_coin(coin))["Data"][0]["Available"]
        paymentId = 1
        if balance > 0:
            if not amount or amount > balance:
                amount = balance - 0.001
            withdraw = json.loads(self.call_withdraw(coin, addr, paymentId, amount))
        if withdraw["Success"] == "True":
            return "Funds successfully withdrawn"
        else:
            return withdraw["Error"]

requester = reqCryptopia()
 