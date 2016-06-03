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

    # Ashley: Added a try catch here-
    # For weird 'Unautherized' error when sending photos.
    # Keeps track of the last user to receive a chat action.
    # Satisfies pending chat actions with a message instead of a photo.
    try:
        googurl = 'https://www.googleapis.com/customsearch/v1'
        args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
                'key': keyConfig.get('Google', 'GCSE_APP_ID'),
                'searchType': "image",
                'safe': "off",
                'q': requestText,
                'searchType': "image"}
        realUrl = googurl + '?' + urllib.urlencode(args)
        data = json.load(urllib.urlopen(realUrl))
        if 'items' in data and len(data['items']) >= 9:
            thereWasAnError = True
            imagelink = 'x-raw-image:///'
            offset = 0
            while thereWasAnError and offset < 10:
                imagelink = data['items'][random.randint(0, 9) + offset]['link']
                offset += 1
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
                thereWasAnError = imagelink.startswith('x-raw-image:///') or \
                                  imagelink == '' or \
                                  not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText, user)
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any images for ' +
                                                      string.capwords(requestText.encode('utf-8')))
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
    except:
        adminGroupId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')
        if user != adminGroupId:
            bot.sendMessage(chat_id=chat_id, text=requestText + ': ' + imagelink)
        if adminGroupId:
            bot.sendMessage(chat_id=adminGroupId, text='Error: ' + str(sys.exc_info()[1]) + '\n' +
                                                  'Request Text: ' + requestText + '\n' +
                                                  'Url: ' + imagelink)



