# coding=utf-8
import ConfigParser
import os
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


    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=en&q='
    realUrl = translateUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['data']['translations']) >= 1:
        translation = data['data']['translations'][0]['translatedText']
        detectedLanguage = data['data']['translations'][0]['detectedSourceLanguage']
        languagesList = json.load(urllib.urlopen(
            'https://www.googleapis.com/language/translate/v2/languages?target=en&key=' + keyConfig.get(
                'Google', 'GCSE_APP_ID')))['data']['languages']
        detectedLanguageSemanticName = [lang for lang in languagesList
                                        if lang['language'] == detectedLanguage][0]['name']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                  "Detected language: " + detectedLanguageSemanticName + \
                                  "\nMeaning: " + translation.title()
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any translations for ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)