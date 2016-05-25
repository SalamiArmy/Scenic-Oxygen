# coding=utf-8
import ConfigParser
import os
import random
import string
import urllib

import telegram
#reverse image search imports:
import json


def run(thorin, update):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(os.getenv("THORIN_API_TOKEN"))

    # chat_id is required to reply to any message
    chat_id = update.message.chat_id
    message = update.message.text
    user = update.message.from_user.username \
        if not update.message.from_user.username == '' \
        else update.message.from_user.first_name + (' ' + update.message.from_user.last_name) \
        if not update.message.from_user.last_name == '' \
        else ''

    message = message.replace(bot.name, "").strip()

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''


    googurl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + keyConfig.get('Google',
                                                                                      'GCSE_APP_ID') + '&q='
    realUrl = googurl + requestText.encode('utf-8') + "&fileType=gif"
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][random.randint(0, 9)]['link']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = imagelink
        bot.sendDocument(chat_id=userWithCurrentChatAction,
                         filename=requestText.encode('utf-8'),
                         document=urlForCurrentChatAction.encode('utf-8'))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find a gif for ' + \
                                  string.capwords(requestText.encode('utf-8')) + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction.encode('utf-8'))