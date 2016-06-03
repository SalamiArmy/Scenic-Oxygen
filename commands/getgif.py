# coding=utf-8
import json
import random
import string
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()

    googurl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=20&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + keyConfig.get('Google',
                                                                                      'GCSE_APP_ID') + '&q='
    realUrl = googurl + requestText.encode('utf-8') + "&fileType=gif"
    data = json.load(urllib.urlopen(realUrl))
    offset = 0
    thereWasAnError = True
    if 'items' in data and len(data['items']) >= 1:
        while thereWasAnError and offset < 10:
            imagelink = data['items'][random.randint(0, 9)+offset]['link']
            offset += 1
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            thereWasAnError = retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find a gif for ' + \
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))

