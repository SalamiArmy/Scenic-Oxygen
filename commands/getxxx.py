# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
#reverse image search imports:
import json


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    googurl = 'https://www.googleapis.com/customsearch/v1?&num=10&safe=off&cx=' + keyConfig.get \
        ('Google', 'GCSE_XSE_ID') + '&key=' + keyConfig.get('Google', 'GCSE_APP_ID') + '&q='
    realUrl = googurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if data['searchInformation']['totalResults'] >= '1':
        for item in data['items']:
            xlink = item['link']
            if \
               'xvideos.com/tags/' not in xlink \
               and 'xvideos.com/favorite/' not in xlink \
               and 'xvideos.com/?k=' not in xlink \
               and 'xvideos.com/tags' not in xlink \
               and 'pornhub.com/users/' not in xlink \
               and 'pornhub.com/video/search?search=' not in xlink \
               and 'xvideos.com/profiles/' not in xlink \
               and 'xnxx.com/?' not in xlink \
               and 'xnxx.com/tags/' not in xlink \
               and 'xhamster.com/stories_search' not in xlink \
               and 'redtube.com/pornstar/' not in xlink \
               :
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                userWithCurrentChatAction = chat_id
                urlForCurrentChatAction = (user + ': ' if not user == '' else '') + xlink
                bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
                break
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', you\'re just too filthy.')