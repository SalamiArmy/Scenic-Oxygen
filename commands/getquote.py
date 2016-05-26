# coding=utf-8
import ConfigParser
import os
import re
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


    wikiUrl = \
        'https://simple.wikiquote.org/w/api.php?action=query&list=search&srlimit=1&namespace=0&format=json&srsearch='
    realUrl = wikiUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['query']['search']) >= 1:
        formattedQuoteSnippet = re.sub(r'<[^>]*?>', '',
            data['query']['search'][0]['snippet'].replace('<span class="searchmatch">', '*').replace(
                '</span>', '*'))
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + formattedQuoteSnippet + \
                                  '\nhttps://simple.wikiquote.org/wiki/' + \
                                  urllib.quote(data['query']['search'][0]['title'].encode('utf-8'))
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction,
                        disable_web_page_preview=True, parse_mode='Markdown')
    else:
        wikiUrl = \
            'https://en.wikiquote.org/w/api.php?action=query&list=search&srlimit=1&namespace=0&format=json&srsearch='
        realUrl = wikiUrl + requestText.encode('utf-8')
        data = json.load(urllib.urlopen(realUrl))
        if len(data['query']['search']) >= 1:
            formattedQuoteSnippet = re.sub(r'<[^>]*?>', '',
                data['query']['search'][0]['snippet'].replace('<span class="searchmatch">', '*').replace(
                    '</span>', '*'))
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + formattedQuoteSnippet + \
                                      '\nhttps://en.wikiquote.org/wiki/' + \
                                      urllib.quote(data['query']['search'][0]['title'].encode('utf-8'))
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction,
                            disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                      ', I\'m afraid I can\'t find any quotes for ' + \
                                      requestText.encode('utf-8') + '.'
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)