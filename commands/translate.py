# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
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
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                              "Detected language: " + detectedLanguageSemanticName + \
                                              "\nMeaning: " + translation.title())
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any translations for ' + \
                                              requestText.encode('utf-8') + '.')