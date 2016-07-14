import ConfigParser
import json
import random
import string
import sys
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            "imgSize": "huge"}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data and len(data['items']) >= 9:
        thereWasAnError = True
        offset = 0
        randint = random.randint(0, 9)
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        while thereWasAnError and offset < 10:
            randint_offset = randint + offset
            imagelink = data['items'][randint_offset if randint_offset < 10 else randint_offset - 10]['link']
            offset += 1
            if not imagelink.startswith('x-raw-image:///') and imagelink != '':
                thereWasAnError = not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText, user)
        if thereWasAnError or not offset < 10:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any huge images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any huge images for ' +
                                              string.capwords(requestText.encode('utf-8')))


