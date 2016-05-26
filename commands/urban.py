# coding=utf-8
import ConfigParser
import os
import random
import string
import urllib

import telegram
#reverse image search imports:
import json


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

    dicurl = 'http://api.urbandictionary.com/v0/define?term='
    realUrl = dicurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'list' in data and len(data['list']) >= 1:
        resultNum = data['list'][random.randint(0, len(data['list']) - 1)]
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') +\
                                  'Urban Definition For ' + string.capwords(requestText.encode('utf-8')) + ":\n" + resultNum['definition'] +\
                                  '\n\nExample:\n' + resultNum['example']
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction ='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                 ', I\'m afraid I can\'t find any urban definitions for ' +\
                                 string.capwords(requestText.encode('utf-8')) + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)
