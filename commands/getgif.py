# coding=utf-8
import json
import random
import string
import urllib
import io
from PIL import Image

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message):
    global gif
    requestText = message.replace(bot.name, "").strip()

    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif'}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    offset = 0
    thereWasAnError = True
    if 'items' in data and len(data['items'])-1 >= 0:
        randint = random.randint(0, len(data['items'])-1)
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        while thereWasAnError and offset < 10:
            randint_offset = randint + offset
            imagelink = data['items'][randint_offset if randint_offset < 10 else randint_offset - 10]['link']
            offset += 1
            print("Openning url " + imagelink)
            fd = urllib.urlopen(imagelink)
            print("Reading gif...")
            image_file = io.BytesIO(fd.read())
            try:
                print("Parsing gif...")
                gif = Image.open(image_file)
            except IOError:
                gif.fp.close()
                print("...not a gif")
                thereWasAnError = True
            else:
                try:
                    print("Checking gif for animation...")
                    gif.seek(1)
                except EOFError:
                    gif.fp.close()
                    print("...not animated")
                    thereWasAnError = True
                else:
                    print("...gif is animated, confirmed!")
                    thereWasAnError = not retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText)
        if thereWasAnError or not offset < 10:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find a gif for ' +
                                                  string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find a gif for ' +
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))

