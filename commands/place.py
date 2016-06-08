# coding=utf-8
import json
import urllib

import telegram


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()


    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['results']) >= 1:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.FIND_LOCATION)
        bot.sendLocation(chat_id=chat_id, latitude=latNum, longitude=lngNum)
    else:
        bot.sendMessage(chat_id=chat_id,
                        text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                             ', I\'m afraid I can\'t find any places for ' + \
                             requestText.encode('utf-8') + '.')