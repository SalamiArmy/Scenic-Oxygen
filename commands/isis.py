# coding=utf-8
import ConfigParser
import os
import random

import feedparser
import telegram




def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    realUrl = 'http://isis.liveuamap.com/rss'
    data = feedparser.parse(realUrl)
    if len(data.entries) >= 1:
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                  data.entries[random.randint(0, 9)].link
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any ISIS news.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)