# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=de&q='
    realUrl = translateUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['data']['translations']) >= 1:
        translation = data['data']['translations'][0]['translatedText']
        bot.sendMessage(chat_id=chat_id, text=(user + ', ' if not user == '' else '') + \
                                              "in German: " + translation)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any translations for ' + \
                                              requestText.encode('utf-8') + '.')