# coding=utf-8
import ConfigParser
import json
import string
import urllib

import telegram


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

    googurl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + keyConfig.get('Google',
                                                                                      'GCSE_APP_ID') + '&q='
    realUrl = googurl + requestText.encode('utf-8') + "&imgSize=huge"
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data:
        imagelink = 'x-raw-image:///'
        offset = 0
        while imagelink.startswith('x-raw-image:///') and offset < 10 and offset < len(data['items']):
            imagelink = data['items'][offset]['link']
            offset = offset + 1
        if not imagelink.startswith('x-raw-image:///'):
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            bot.sendPhoto(chat_id=chat_id, photo=imagelink.encode('utf-8'),
                          caption=(user + ': ' if not user == '' else '') +
                                  requestText.title().encode('utf-8') +
                                  (' ' + imagelink if len(imagelink) < 100 else ''))
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                  ', I\'m afraid I can\'t find a huge image for ' + \
                                                  string.capwords(requestText.encode('utf-8')) + '.')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find a huge image for ' + \
                                              string.capwords(requestText.encode('utf-8')) + '.')