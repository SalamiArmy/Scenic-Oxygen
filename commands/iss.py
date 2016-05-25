# coding=utf-8
import ConfigParser
import datetime
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

    if requestText != '':
        mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
                  keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
        realUrl = mapsUrl + requestText.encode('utf-8')
        data = json.load(urllib.urlopen(realUrl))
        if len(data['results']) >= 1:
            latNum = data['results'][0]['geometry']['location']['lat']
            lngNum = data['results'][0]['geometry']['location']['lng']
            issSightingsUrl = 'http://api.open-notify.org/iss-pass.json?lat='
            realUrl = issSightingsUrl + str(latNum) + '&lon=' + str(lngNum)
            data = json.load(urllib.urlopen(realUrl))
            if len(data['response']) >= 1:
                timeStamp = data['response'][0]['risetime']
                durationSeconds = data['response'][0]['duration']
                startDateTime = datetime.datetime.fromtimestamp(timeStamp)
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                userWithCurrentChatAction = chat_id
                urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                          'The next ISS sighting in ' + requestText.encode('utf-8').title() + \
                                          ' starts at ' + startDateTime.strftime('%H:%M:%S on %d-%m-%Y') + \
                                          ' for ' + str(divmod(durationSeconds, 60)[0]) + \
                                          ' minutes and ' + str(divmod(durationSeconds, 60)[1]) + ' seconds.'
                bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
            else:
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                userWithCurrentChatAction = chat_id
                urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                          ', I\'m afraid I can\'t find the next ISS sighting for ' + \
                                          requestText.encode('utf-8') + '.'
                bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                      ', I\'m afraid I can\'t find any places for ' + \
                                      requestText.encode('utf-8') + '.'
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=requestText)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=400&height=400&satid=25544'
        bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=urlForCurrentChatAction,
                       caption='Current Position of the ISS')