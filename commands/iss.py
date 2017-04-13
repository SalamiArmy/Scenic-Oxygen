import datetime
import json
import urllib
import uuid

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    if requestText != '':
        has_iss_results, has_place_results, startDateTime, durationSeconds = get_iss_data(keyConfig, requestText)
        if has_place_results:
            if has_iss_results:
                bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                                      format_iss_message(durationSeconds, requestText, startDateTime))
                return True
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


def format_iss_message(durationSeconds, requestText, startDateTime):
    return 'The next ISS sighting in ' + requestText.encode('utf-8').title() + ' starts at ' + startDateTime.strftime(
        '%H:%M:%S on %d-%m-%Y') + ' for ' + str(divmod(durationSeconds, 60)[0]) + ' minutes and ' + str(
        divmod(durationSeconds, 60)[1]) + ' seconds.'


def get_iss_data(keyConfig, requestText):
    durationSeconds = ''
    startDateTime = datetime.datetime.fromtimestamp(0)
    has_iss_results = False
    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    has_place_results = len(data['results']) >= 1
    if has_place_results:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        issSightingsUrl = 'http://api.open-notify.org/iss-pass.json?lat='
        realUrl = issSightingsUrl + str(latNum) + '&lon=' + str(lngNum)
        data = json.load(urllib.urlopen(realUrl))
        has_iss_results = len(data['response']) >= 1
        if has_iss_results:
            timeStamp = data['response'][0]['risetime']
            durationSeconds = data['response'][0]['duration']
            startDateTime = datetime.datetime.fromtimestamp(timeStamp)
    return has_iss_results, has_place_results, startDateTime, durationSeconds
