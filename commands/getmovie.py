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


    movieUrl = 'http://www.omdbapi.com/?plot=short&r=json&y=&t='
    realUrl = movieUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'Error' not in data:
        if 'Poster' in data and not data['Poster'] == 'N/A':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = data['Poster']
            bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=urlForCurrentChatAction,
                          caption=(user if not user == '' else '') + data['Title'] + ':\n' + data['Plot'])
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      data['Title'] + ':\n' + data['Plot']
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any movies for ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)