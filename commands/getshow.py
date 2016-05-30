# coding=utf-8
import json
import re
import urllib

import telegram


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()


    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
    if len(data) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=chat_id,
                      photo=data[0]['show']['image']['original'],
                      caption=re.sub(r'<[^>]*?>', '', data[0]['show']['summary'].replace('\\', '')[:125]))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I cannot find the TV show ' + \
                                              requestText.title())