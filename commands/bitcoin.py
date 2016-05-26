# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
#reverse image search imports:
import json


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    data = json.load(urllib.urlopen(bcurl))
    bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data2 = json.load(urllib.urlopen(bcurl2))
    updateTime = data['time']['updated']
    priceUS = data['bpi']['USD']
    priceZA = data['bpi']['ZAR']
    priceGB = data2['bpi']['GBP']
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS['rate'] +
                         ' USD\n' + priceGB['rate'] +
                         ' GBP\n' + priceZA['rate'] + ' ZAR' + '\n\nTime Updated: ' + updateTime)