# coding=utf-8
import random

import feedparser


def run(bot, keyConfig, chat_id, user, message):
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