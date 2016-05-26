# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
import json


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    vidurl = 'https://www.googleapis.com/youtube/v3/search?safeSearch=none&type=video&key=' + keyConfig.get \
        ('Google', 'GCSE_APP_ID') + '&part=snippet&q='
    realUrl = vidurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data and len(data['items']) >= 1:
        vidlink = data['items'][0]['id']['videoId']
        userWithCurrentChatAction = chat_id
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                              'https://www.youtube.com/watch?v=' + vidlink + '&type=video')
    else:
        userWithCurrentChatAction = chat_id
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t do that.\n(Video not found)')