# coding=utf-8
import json
import urllib


def run(bot, keyConfig, chat_id, user, message):
    usdurl = 'http://api.fixer.io/latest?base=USD'
    gbpurl = 'http://api.fixer.io/latest?base=GBP'
    eururl = 'http://api.fixer.io/latest?base=EUR'
    data1 = json.load(urllib.urlopen(usdurl))
    data2 = json.load(urllib.urlopen(gbpurl))
    data3 = json.load(urllib.urlopen(eururl))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    bot.sendMessage(chat_id=chat_id, text='1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + \
                                          ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR')
    return True