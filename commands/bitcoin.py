# coding=utf-8
import json
import urllib


def run(bot, keyConfig, chat_id, user, message):
    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    data = json.load(urllib.urlopen(bcurl))
    bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data2 = json.load(urllib.urlopen(bcurl2))
    updateTime = data['time']['updated']
    priceUS = data['bpi']['USD']
    priceZA = data['bpi']['ZAR']
    priceGB = data2['bpi']['GBP']
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS['rate'] +
                         ' USD\n' + priceGB['rate'] +
                         ' GBP\n' + priceZA['rate'] + ' ZAR' + '\n\nTime Updated: ' + updateTime)
    return True
