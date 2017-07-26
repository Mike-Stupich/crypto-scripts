import json
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bittrex import Bittrex

class bittrexTracker():
    def setup(self):
        with open("apikeys.json") as apikeys:
            self.keys = json.load(apikeys)
            apikeys.close()
        self.bittrex = Bittrex(self.keys['key'], self.keys['secret'])

    #Have to withdraw from pool or wallet here
    def depositFunds(self, address):
        print(address)

    #Check wallet to see if funds arrived, once they have sell at price
    def sellFundsOnceArrived(self, coin, price):
        print(coin)

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
            print(coin_found);
            if coin_found != "NOT FOUND":
                break
            time.sleep(5)
        #When found keep trying to get addr - Needs to generate on first attempt
        while True:
            try:
                addr = self.bittrex.get_deposit_address(coin)['result']['Address']
            except (TypeError):
                print("Generating address... trying again in 2 seconds")
                time.sleep(2)
            else:
                break
        #self.depositFunds(addr)
        self.sendNotification(coin, addr)

notifier = bittrexTracker()
notifier.setup()
notifier.checkIfListed('SIGT')
