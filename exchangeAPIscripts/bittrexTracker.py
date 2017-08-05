import json
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bittrex import Bittrex
from req_cryptopia import reqCryptopia

class bittrexTracker():
    def __init__(self):
        with open("apikeys.json") as apikeys:
            self.keys = json.load(apikeys)
            apikeys.close()
        for key in self.keys['APIs']:
            if key['exchange'] == 'Bittrex':
                self.bittrex = Bittrex(key['key'], key['secret'])
        self.cryptopia = reqCryptopia()
        
    #Withdraw funds from cryptopia wallet to address
    def depositFunds(self, coin, address):
        self.cryptopia.handle_withdraw(coin, address)

    #Check wallet to see if funds arrived, once they have sell at price
    def sellFundsOnceArrived(self, coin, price, amount=None):
        while True:
            status = "TRANSFER IN PROGRESS"
            curr_balance = self.bittrex.get_balance(coin)
            bal = curr_balance["result"]["Available"]
            if bal > 0:
                status = "Funds have arrived"
                break
            else:
                print(status)
            time.sleep(1)
        print(status + ", " + bal + coin + "in account")
        
        market = "BTC-" + coin
        if amount and amount <= bal:
            print(self.bittrex.sell_limit(market, amount, price))
        else:
            print(self.bittrex.sell_limit(market, bal, price))

    def sendNotification(self, coin, addr):
        with open("emaillogin.json") as loginInfo:
            self.info = json.load(loginInfo)
            loginInfo.close()

        COMMASPACE = ', '
        fromaddr = "mike.stupich@gmail.com"
        toaddr = ["mike.stupich@gmail.com"]
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = COMMASPACE.join(toaddr)
        msg['Subject'] = coin + " has been added to Bittrex"
        body = coin + " Address: " + addr
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.info['user'], self.info['pass'])
        message = msg.as_string()
        server.sendmail(fromaddr,toaddr,message)

    def checkIfListed(self, coin):
        while True:
            coin_found = "NOT FOUND"
            curr_markets = self.bittrex.get_currencies()
            currencies = curr_markets["result"]
            for res in currencies:
                if res['Currency'] == coin:
                    coin_found = res
            print(coin_found)
            if coin_found != "NOT FOUND":
                break
            time.sleep(30)
        #When found keep trying to get addr - Needs to generate on first attempt
        while True:
            try:
                addr = self.bittrex.get_deposit_address(coin)['result']['Address']
            except (TypeError):
                print("Generating address... trying again in 2 seconds")
                time.sleep(2)
            else:
                break
        self.sendNotification(coin, addr)
        self.depositFunds(coin, addr)
        self.sellFundsOnceArrived(coin, 0.00005000)

notifier = bittrexTracker()
notifier.checkIfListed('SIGT')
