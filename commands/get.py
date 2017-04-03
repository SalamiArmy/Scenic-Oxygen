# coding=utf-8
import json
import random
import string
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = Google_Image_Search(keyConfig, requestText)
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
                thereWasAnError = not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText, user, intention_confidence)
        if (thereWasAnError or not offset < 10) and intention_confidence == 0.0:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
        else:
            return True
    else:
        if intention_confidence == 0.0:
            if 'error' in data:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      data['error']['message'])
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any images for ' +
                                                      string.capwords(requestText.encode('utf-8')))


def Google_Image_Search(keyConfig, requestText):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': requestText}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    return data


