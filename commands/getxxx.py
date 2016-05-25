# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
#reverse image search imports:
import json


def run(thorin, update):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(os.getenv("THORIN_API_TOKEN"))

    # chat_id is required to reply to any message
    chat_id = update.message.chat_id
    message = update.message.text
    user = update.message.from_user.username \
        if not update.message.from_user.username == '' \
        else update.message.from_user.first_name + (' ' + update.message.from_user.last_name) \
        if not update.message.from_user.last_name == '' \
        else ''

    message = message.replace(bot.name, "").strip()

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''


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