# coding=utf-8
import ConfigParser
import os
import urllib
import json


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()


    usdurl = 'http://api.fixer.io/latest?base=USD'
    gbpurl = 'http://api.fixer.io/latest?base=GBP'
    eururl = 'http://api.fixer.io/latest?base=EUR'
    data1 = json.load(urllib.urlopen(usdurl))
    data2 = json.load(urllib.urlopen(gbpurl))
    data3 = json.load(urllib.urlopen(eururl))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = '1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + \
                              ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR'
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)