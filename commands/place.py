# coding=utf-8
import ConfigParser
import os
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


    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['results']) >= 1:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.FIND_LOCATION)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'lat=' + str(latNum) + ' long=' + str(lngNum)
        bot.sendLocation(chat_id=chat_id, latitude=latNum, longitude=lngNum)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any places for ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)