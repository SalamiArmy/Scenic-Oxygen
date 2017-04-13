# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    priceGB, priceUS, priceZA, updateTime = get_bitcoin_prices()
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS +
                         ' USD\n' + priceGB +
                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
    return True


def get_bitcoin_prices():
    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    data = json.load(urllib.urlopen(bcurl))
    bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data2 = json.load(urllib.urlopen(bcurl2))
    updateTime = data['time']['updated']
    priceUS = data['bpi']['USD']['rate']
    priceZA = data['bpi']['ZAR']['rate']
    priceGB = data2['bpi']['GBP']['rate']
    return priceGB, priceUS, priceZA, updateTime
