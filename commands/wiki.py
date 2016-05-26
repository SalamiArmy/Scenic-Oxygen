# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
import json


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    wikiUrl = \
        'https://simple.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
    realUrl = wikiUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data[2]) >= 1:
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                  data[2][0] + '\nLink: ' + data[3][0]
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction, disable_web_page_preview=True)
    else:
        wikiUrl = \
            'https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
        realUrl = wikiUrl + requestText.encode('utf-8')
        data = json.load(urllib.urlopen(realUrl))
        if len(data[2]) >= 1 and not data[2][0] == '':
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      data[2][0] + '\nLink: ' + data[3][0]
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction,
                            disable_web_page_preview=True)
        else:
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                      ', I\'m afraid I can\'t find any wiki articles for ' + \
                                      requestText.encode('utf-8') + '.'
            bot.sendMessage(chat_id=userWithCurrentChatAction,
                            text=urlForCurrentChatAction)