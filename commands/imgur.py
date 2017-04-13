# coding=utf-8
import random
import string

import telegram
from imgurpython import ImgurClient


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    client_id = keyConfig.get('Imgur', 'CLIENT_ID')
    client_secret = keyConfig.get('Imgur', 'CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)
    items = client.gallery_search(q=requestText,
                                  sort='top',
                                  window='all',
                                  page=1)
    if len(items) > 0:
        for item in items:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            bot.sendDocument(chat_id=chat_id,
                             filename=requestText.encode('utf-8'),
                             document=item.link.encode('utf-8'))
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any Imgur images for ' +
                                              string.capwords(requestText.encode('utf-8')))