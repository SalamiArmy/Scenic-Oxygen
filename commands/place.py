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
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any places for ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)