# coding=utf-8
import json
import random
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message):
    realUrl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&q=fig'
    data = json.load(urllib.urlopen(realUrl))
    if data['searchInformation']['totalResults'] >= 1:
        imagelink = data['items'][random.randint(0, 9)]['link']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, '', user)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any figs.')