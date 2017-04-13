# coding=utf-8
import random

import feedparser


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    realUrl = 'http://isis.liveuamap.com/rss'
    data = feedparser.parse(realUrl)
    if len(data.entries) >= 1:
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                              data.entries[random.randint(0, 9)].link)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any ISIS news.')