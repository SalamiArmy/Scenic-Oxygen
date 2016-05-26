# coding=utf-8
import ConfigParser
import os
import random
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


    realUrl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&q=fig'
    data = json.load(urllib.urlopen(realUrl))
    if data['searchInformation']['totalResults'] >= 1:
        imagelink = data['items'][random.randint(0, 9)]['link']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = imagelink.encode('utf-8')
        bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=urlForCurrentChatAction,
                      caption=(user if not user == '' else '') +
                              (' ' + imagelink if len(imagelink) < 100 else ''))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any figs.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)