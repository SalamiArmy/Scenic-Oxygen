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

    giphyUrl = 'http://api.giphy.com/v1/gifs/search?q='
    apiKey = '&api_key=dc6zaTOxFJmzC&limit=10&offset=0'
    realUrl = giphyUrl + requestText.encode('utf-8') + apiKey
    data = json.load(urllib.urlopen(realUrl))
    if data['pagination']['total_count'] >= 1:
        imagelink = data['data'][random.randint(0, len(data['data']) - 1)]['images']['original']['url']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = imagelink
        bot.sendDocument(chat_id=userWithCurrentChatAction,
                         filename=requestText.encode('utf-8') + '.gif',
                         document=urlForCurrentChatAction.encode('utf-8'))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find a giphy gif for ' + \
                                  string.capwords(requestText.encode('utf-8')) + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction.encode('utf-8'))