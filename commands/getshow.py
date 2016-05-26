# coding=utf-8
import ConfigParser
import os
import re
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


    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
    if len(data) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        urlForCurrentChatAction = data[0]['show']['image']['original']
        bot.sendPhoto(chat_id=chat_id,
                      photo=urlForCurrentChatAction,
                      caption=re.sub(r'<[^>]*?>', '', data[0]['show']['summary'].replace('\\', '')[:125]))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I cannot find the TV show ' + \
                                  requestText.title()
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)