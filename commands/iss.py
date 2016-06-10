import datetime
import json
import urllib
import uuid

import telegram
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()

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
                bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                                      'The next ISS sighting in ' +
                                                      requestText.encode('utf-8').title() +
                                                      ' starts at ' + startDateTime.strftime('%H:%M:%S on %d-%m-%Y') +
                                                      ' for ' + str(divmod(durationSeconds, 60)[0]) + ' minutes and ' +
                                                      str(divmod(durationSeconds, 60)[1]) + ' seconds.')
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find the next ISS sighting for ' +
                                                      requestText.encode('utf-8') + '.')
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any places for ' +
                                                  requestText.encode('utf-8') + '.')
    else:
        url = 'http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=400&height=400&satid=25544&uuid=' + \
              str(uuid.uuid4())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendMessage(chat_id=chat_id, text=url)
