# coding=utf-8
import json
import urllib

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    movieUrl = 'http://www.omdbapi.com/?plot=short&r=json&y=&t='
    realUrl = movieUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'Error' not in data:
        if 'Poster' in data and not data['Poster'] == 'N/A':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            bot.sendPhoto(chat_id=chat_id, photo=data['Poster'].encode('utf-8'),
                          caption=(user if not user == '' else '') + data['Title'] + ':\n' + data['Plot'][400:])
            return True
        else:
            bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                      data['Title'] + ':\n' + data['Plot'])
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any movies for ' +
                                              requestText.encode('utf-8') + '.')