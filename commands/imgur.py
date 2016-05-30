# coding=utf-8
import ConfigParser
import os
import random
import string

from imgurpython import ImgurClient


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()

    client_id = keyConfig.get('Imgur', 'CLIENT_ID')
    client_secret = keyConfig.get('Imgur', 'CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)
    items = client.gallery_search(q=string.capwords(requestText.encode('utf-8')),
                                  advanced={'q_type': 'anigif'},
                                  sort='top',
                                  window='all',
                                  page=random.randint(0, 9))
    for item in items:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendDocument(chat_id=chat_id,
                         filename=requestText.encode('utf-8'),
                         document=item.link.encode('utf-8'))